#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip install camelot-py[cv]
#camelot-pyにはghostscriptインストール必要→https://www.ghostscript.com/download/gsdnld.html
# pip install japanize-matplotlib #今回はskip
import sys
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import japanize_matplotlib
import camelot
from pathlib import Path
import datetime
now = datetime.datetime.now()
now = now.strftime("%y%m%d")

### 指定した列の要素の中身を調べた後に、各々の数を数えて、並び替える関数
def count_in_special_column(DF, check_column):
    df = DF.dropna(subset=[check_column])
    df = df.dropna(axis=1)
    df = df.groupby([check_column]).size()
    df = df.reset_index(name='count')
    df = df.sort_values(by='count', ascending=True)
    
    return df

### 横棒グラフ化する関数。引数Xはカウントする列名、引数Yは数えた数（'count'）
#def xy_plot(DF, X, Y):
#    print(DF)
#    df_x = DF[X]
#    df_y = DF[Y]
#    
#    y_np = np.array(df_y)
#    plt.figure(figsize=(8,10))
#    plt.barh(range(len(df_x)), df_y, tick_label=df_x, align="center", color="magenta", height=0.8)
#    for i, j in enumerate(y_np):
#        plt.text(j, (i+0.5), str(int(j)), ha='left', va='top')
#    #plt.title()
#    plt.xlabel('count', fontsize=10)
#    if range_X:
#        plt.xlim([range_X[0], range_X[1]])
#    plt.grid(which="major", axis="x", color="black", alpha=0.8, linestyle="-", linewidth=1)
#    plt.tight_layout()
#    #plt.show()
#    fig_name = now + "_" + file_name + ".png"
#    plt.savefig(fig_name)

def main():
    # pdfファイルの1頁から最終頁までリストで取得する
    tables = camelot.read_pdf(path_pdf, pages='1-end', split_text=True, strip_text='\n')

    dfs = []
    for table in tables: # 1頁毎にDataFrame形式に変換後、リストへ追記してゆく
        print(table.df)
        df = table.df
        dfs.append(df)
    df_all = pd.concat(dfs) # リストの各要素（各頁）を結合
    
    # csvファイルへ出力
    df_all.to_csv(file_name + '.csv', index=False, header=False, encoding='utf-8')
    
    # excelファイルへ出力
    with pd.ExcelWriter(file_name + '.xlsx') as writer:
        df_all.to_excel(writer, sheet_name='sheet1', index=False, header=False)

    df2 = pd.read_csv(file_name + '.csv', header=0, index_col=0)
    #print(df2)

    df3 = count_in_special_column(df2, target_column)
    #xy_plot(df3, target_column, 'count')

if __name__ == '__main__':
    args = sys.argv
    path_pdf = args[1]
    target_column = '項 番'
    range_X = ()
    
    file_name = Path(path_pdf).stem #ファイルパスから、拡張子抜きファイル名を取得
    
    main()