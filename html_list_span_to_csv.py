#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib3
from bs4 import BeautifulSoup
import certifi
import re
import pandas as pd

#技術概要
#url = "https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan03.html"
#医療機関一覧
url = "https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan02.html"

def table_to_2d(table_tag):
    rows = table_tag("tr")
    cols = rows[0](["td", "th"])
    print(str(len(cols)))
    print(str(len(rows)))
    table = [[None] * len(cols) for _ in range(len(rows))]
    for row_i, row in enumerate(rows):
        for col_i, col in enumerate(row(["td", "th"])):
            insert(table, row_i, col_i, col)
    return table

def insert(table, row, col, element):
    if row >= len(table) or col >= len(table[row]):
        return
    if table[row][col] is None:
        value = element.get_text()
        table[row][col] = value
        if element.has_attr("colspan"):
            span = int(element["colspan"])
            for i in range(1, span):
                table[row][col+i] = value
        if element.has_attr("rowspan"):
            span = int(element["rowspan"])
            for i in range(1, span):
                table[row+i][col] = value
    else:
        insert(table, row, col + 1, element)

# httpsの証明書検証を実行している
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())
r = http.request('GET', url)

soup = BeautifulSoup(r.data, 'html.parser')
#soup.find_all("br").decompose()
#scriptタグに囲まれた文字を除去
for tag in soup.find_all("script"):
    tag.decompose()

symbols = ['S','K']

#table = soup.find_all("table")
for i in range(1,3):
    print(str(i))
    tab = soup.select_one("#contentsInner > div:nth-child(" + str(i) + ") > div.prt-table > table")
    #tab = soup.select_one("#contentsInner > div:nth-child(1) > div.prt-table > table")
#    print(tab)
#    break
    table_to_2d(tab)

    df = pd.DataFrame(table_to_2d(tab))
    #1行目を行タイトルに設定
    df.columns = df.iloc[0]
    df.reindex(df.index.drop(0))
    #1行目が空白の場合列を削除
    for c_i, col in enumerate(df.columns):
        if not col.strip():
            df.drop(df.columns[c_i], axis=1, inplace=True)
    #1列目にsymbolsの内容を挿入
    df.insert(0,'',symbols[i-1])
    df.to_csv('out' + str(i) + '.csv', sep=',', encoding='utf-8', header=True, index=False)
