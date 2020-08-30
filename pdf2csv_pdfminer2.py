#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import re           #正規表現
from operator import attrgetter
from pathlib import Path
import datetime
import numpy as np

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LTTextContainer
from pdfminer.layout import LTLine

now = datetime.datetime.now()
now = now.strftime("%y%m%d%H%M%S")

DEBUG = True
QUOTE = True

# magic number
title_name   = "コード内容別医療機関一覧表"
colmuns_name = ["項番", "医療機関番号", "医療機関名称", "医療機関所在地", "電話番号", "勤務医数", "開設者氏名", "管理者氏名", "指定年月日", "登録理由", "指定期間始", "備考"]
columns_x = [0] * 12
#column_count = 6 # 列の数

def table_col_range(layout):

    start_index = 0

    for i, col in enumerate(colmuns_name):
        for l in layout:
            #print(l.index)
            if isinstance(l, LTTextBoxHorizontal) and colmuns_name[i] in re.sub(" |　", '',l.get_text()):
                if start_index == 0:
                    start_index = l.index
                columns_x[colmuns_name.index(col)] = [l.x0,l.x1]
                continue
                
            #if isinstance(l, LTLine) and max_x <l.x1:
            #    max_x = l.x1
    
    return start_index

def tel_divide_array(txt,io_cells):

    pattern = r'\(?\d{2,4}[-)]*\d{2,4}-\d{3,4}.*'
    
    result = re.finditer(pattern, txt)

    for r in result:
        io_cells.append(txt[r.start():r.end()])

    return io_cells

def not_tel_divide_array(txt,io_cells):

    pattern = r'\(?\d{2,4}[-)]*\d{2,4}-\d{3,4}.*'
    
    result = re.finditer(pattern, txt)
    
    bf_end = 0
    for r in result:
        if bf_end !=0:
            io_cells.append(txt[bf_end:r.start()-1])
        bf_end = r.end()
        
    io_cells.append(txt[bf_end:])

    return io_cells

def remove_title_str(txt):

    rmv_str = re.sub(" |　|/|／", '', txt)
    for col_nm in colmuns_name:
        rmv_str = re.sub(r''+ col_nm +'\n?','',rmv_str)

    return rmv_str

def get_table_cells(layout, columns_x):


    #enumerate(columns_x)
    
    rows = np.empty(1)
    for i, col_x in enumerate(columns_x):
        #print(col_x)
        columns = list(filter(lambda c: (issubclass(c.__class__, LTTextBoxHorizontal)
                                         and (   (col_x[0] < c.x0 and c.x0 < col_x[1]) 
                                              or (c.x0 <= col_x[0] and col_x[0] < c.x1)
                                             )
                                         #and not(colmuns_name[i] in re.sub(" |　", '',c.get_text()))
                                        ), layout))
        # print(columns)
        
        cells = list()
        
        for col in columns:
            fil_txt = remove_title_str(col.get_text())
            if colmuns_name[i] in re.sub(" |　", '', col.get_text()):
                cells.append(colmuns_name[i])
                
            #タイトルテキストに行の値が含まれてない場合
            if len(fil_txt) != 0:
                if i <= 1:
                    cells.append(col.get_text().split(' ')[i])
                elif i == 4:
                    # cells.append(colmuns_name[4])
                    tel_divide_array(col.get_text(), cells)
                elif i == 5:
                    not_tel_divide_array(col.get_text(), cells)
                elif 8 <= i and i <=10:
                    cells.append(fil_txt.split('\n')[i % 8])
                else:
                    cells.append(col.get_text())
                #print(cells)

        if i == 0:
            rows = np.array(cells)
        else:
            print('i:'+str(i))
            print(rows)
            print(cells)
            rows = np.vstack([rows, cells])
    
    return rows
    
def main():

    # Open a PDF file.
    fp = open(filename, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    document = PDFDocument()
    parser.set_document(document)

    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    password=""
    document.set_parser(parser)
    document.initialize(password)

    # Get the outlines of the document. #pdfminer.pdfparser.PDFNoOutlinesエラー発生のためコメントアウト
    #outlines = document.get_outlines()
    #for (level,title,dest,a,se) in outlines:
    #    print (level, title)

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    pages = list(document.get_pages())
    
    rows = list()
    for page in pages:
        # interpreter page1
        interpreter.process_page(page)
        
        # receive the LTPage object for the page.
        # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
        layout = device.get_result()
        
        print(layout)
        start_index = table_col_range(layout)
        print(columns_x)
        #print('max_x:' + str(max_x))
        print('start_index:' + str(start_index))
        
        fil_layout = list(filter(lambda c: issubclass(c.__class__, LTTextBoxHorizontal) and start_index <= c.index, layout))
        
        print(fil_layout)
        #break
        
        rows = get_table_cells(fil_layout,columns_x)
        
        print(rows)
        
        df = pd.DataFrame(rows.T)
        #df = pd.DataFrame(rows)
        
        df_csv = df.replace(to_replace=r'\n', value="￥ｎ", regex=True)
        df_csv.to_csv("pdfminer"+ now+ ".csv")
        
        #if layout.pageid == 1:
        #    titles = filter(lambda c: issubclass(c.__class__, LTTextBoxHorizontal), layout)
        #    print(list(titles))
        #    print('max_x:')
        #    print(sorted(layout, key = attrgetter('x0'), reverse=False))


        if layout.pageid > 2:
                break

        for l in layout:
            #print(l)
            #print('\n')
            if isinstance(l, LTTextBoxHorizontal):
                #print('LTTextBoxHorizontal' + l.get_text()) # オブジェクト中のtextのみ抽出
                #print(l)
                #rows.append(sorted(l, key = attrgetter('x0'), reverse=False))
                continue

            elif isinstance(l, LTLine):
                continue
                #print(l) # オブジェクト中のtextのみ抽出
            else:
                # print(l)
                continue


    #print(rows)
    
    device.close()
    fp.close


if __name__ == '__main__':

    if DEBUG:
        print(sys.argv)

    if ( len(sys.argv) > 1 ):
        filename = sys.argv[1]
        file_name = Path(filename).stem #ファイルパスから、拡張子抜きファイル名を取得
    else:
        exit(-1)
    
    main()