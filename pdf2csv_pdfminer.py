#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
#import pandas as pd
import re
from operator import attrgetter
from pathlib import Path
import datetime
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextContainer, LTTextBox
from pdfminer.pdfpage import PDFPage


now = datetime.datetime.now()
now = now.strftime("%y%m%d%H%M%S")

DEBUG = True
QUOTE = True

# magick number
range_violation_col = (142,778)
range_first_col = (28, 141 )
range_column_last = (779, 799 )
#column_count = 6 # 列の数


def format_list_cell(node) :
    temp_str = node.get_text().rstrip("\n")

    # 違反した条文を列挙しているカラムの処理
    #if "条" in temp_str :
    #    src_str = re.sub(r'(?<=(条|\d))\n(?!(の|$))', ',', temp_str)
    #else:
    #    src_str = temp_str.replace("\n",',')

    #str = src_str.replace("\n",'')
    str = temp_str.replace("\n",'￥ｎ')
    return str

def remove_returncode(node) :
    src_str = node.get_text()
    
    if 'H' in src_str :
        src_str = re.sub(r'\n(?=H)', ',', src_str)
    

    str = src_str.replace("\n", '')
    

    if DEBUG :
        print('remove_returncode:' + str)

    return str


rsrcmgr = PDFResourceManager()
laparams = LAParams()

#laparams.detect_vertical = True

def main():

    device = PDFPageAggregator(rsrcmgr, laparams=laparams)


    # 処理するPDFを開く
    fp = open(filename, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)


    parser = PDFParser(fp)
    document = PDFDocument(parser, '')

    dept_labor = "" # 都道府県労働局
    last_modified_date = ""

    header_text = ["項 番", "医 療 機 関 番 号", "医 療 機 関 名 称", "医療機関所在地", "開設者氏名", "管理者氏名", "指定年月日","登録理由","指定期間始","備　考","電話番号 ／勤務医数","病床数　／診療科名"  ]

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # page.contents
        layout = device.get_result()

        if DEBUG :
            print(layout.pageid)

        #if (layout.pageid == 1 ) :
        #    continue


        cells = list()


        for node in layout:
            if ( not issubclass(node.__class__ ,(LTTextBox, LTTextContainer ) ) ):
                
                if DEBUG:
                    print(node)
                continue
            else:

                temp_str = node.get_text().rstrip("\n") 
                if temp_str.endswith("作成") :
                    #last_modified_date = temp_str[6:]
                    last_modified_date = temp_str
                    if DEBUG :
                        print('作成日:' + last_modified_date)
                    continue
                if temp_str.endswith("県") :
                    dept_labor = temp_str
                    continue
                if temp_str.endswith("公表事案") :
                    continue

                cells.append(node)

        filtered_cells = list(filter(lambda c: not(c.get_text().rstrip() in header_text) , cells))

        header_cells = list(filter(lambda c: c.get_text().rstrip() in header_text , cells))


        temp_cells = sorted(filtered_cells, key = attrgetter('x0'), reverse=False)
        sorted_cells = sorted(temp_cells, key = lambda c: (c.y0 + c.y1) // 20, reverse=True)
        #sorted_cells = sorted(temp_cells, key = attrgetter('y0'), reverse=True)
        #sorted_cells = sorted(temp_cells, key = attrgetter('x0'), reverse=False)

        
        columns = list()
        for cell in sorted_cells :
            if DEBUG:
                print(cell)

            center_x = ( cell.x0 + cell.x1 ) / 2.0
            #if ( center_x > range_first_col[0] and center_x < range_first_col[1] ) :
            if ( center_x > range_first_col[0] and cell.x0 < range_first_col[1] ) :
                # 先頭
                col_str = remove_returncode(cell)
                if ( cell.x1 < range_first_col[1] and ' ' in col_str ) :
                    col_str = re.sub(' +', '　', col_str)
                    print(col_str, file=sys.stderr)
               
                columns.insert(0, col_str)

            elif ( center_x > range_column_last[0] and center_x < range_column_last[1] ):
                # 最終カラム
                col_str = remove_returncode(cell)

                columns.append(col_str)


                # 出力

                # clean up
                purificated = list()
                for st in columns:
                    if DEBUG:
                        print(st)

                    if st.endswith("　") :
                        st = st.rstrip("　") # 末尾の全角空白を削除

                    if re.search('  ',st):
                        # 半角空白の連続は全角スペースに
                        st = st.replace('  ',"\u3000")

                    # 正常にパースできなかったセルを半角スペースで分割
                    if (' ' in st ) and ( not '確定' in st ):
    #                    temp = st.split(' ')
                        if re.search('(都|道|府|県).+(市|町|村)' ,st) :
                            if '条' in st :
                                # カラムが4つ結合しているケース
                                temp = st.rsplit(" ",3)
                            elif 'H' in st :
                                # カラムが3つ結合しているケース
                                temp = st.rsplit(" ",2)
                            else:
                                # カラムが2つ結合しているケース
                                temp = st.rsplit(" ",1)
                        else:
                            temp = re.split('(?<!）) ',st)

                        for ts in temp :
                            purificated.append(ts)
                    else:
                        purificated.append(st)


                output = dept_labor + "\t" + last_modified_date + "\t" + "\t".join(purificated)
                if QUOTE:
                    temp = list(map( lambda x: '"%s"' % x, output.split("\t") ))
                    output = "\t".join(temp)

                print(output)
                columns = list()


            else:
                # それ以外
                if  center_x > range_violation_col[0]  and  center_x < range_violation_col[1]  :
                    col_str = format_list_cell(cell)
                else:
                    col_str = remove_returncode(cell)
                
                columns.append(col_str)



    fp.close()
    device.close()

if __name__ == '__main__':

    if DEBUG:
        print(sys.argv)

    if ( len(sys.argv) > 1 ):
        filename = sys.argv[1]
        file_name = Path(filename).stem #ファイルパスから、拡張子抜きファイル名を取得
    else:
        exit(-1)
    
    main()