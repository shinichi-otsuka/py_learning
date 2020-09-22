#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd

""" テーブルtagを二次元配列に設定して戻す """


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


""" 再起的に呼び出しながら指定のelementを二次元配列tableに設定（rowspan,colspanを考慮） """


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


class htmltable_scraping:
    def __init__(self, url=None, css_selector=None, symbols=['S', 'K'], csv_file_name='out'):
        self.__url = url
        self.__css_selector = css_selector
        self.__symbols = symbols
        self.__csv_file_name = csv_file_name

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def css_selector(self):
        return self.__css_selector

    @css_selector.setter
    def css_selector(self, css_selector):
        self.__css_selector = css_selector

    @property
    def symbols(self):
        return self.__symbols

    @symbols.setter
    def symbols(self, symbols):
        self.__symbols = symbols

    @property
    def csv_file_name(self):
        return self.__csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, csv_file_name):
        self.__csv_file_name = csv_file_name

    def html_to_csv(self):
        url = self.url
        if url is None:
            raise Exception('url is None')
        # httpsの証明書検証を実行している
        # http = urllib3.PoolManager(
        #    cert_reqs='CERT_REQUIRED',
        #    ca_certs=certifi.where())
        # r = http.request('GET', url)
        # soup = BeautifulSoup(r.data, 'html.parser')

        # 文字化けしないようエンコーディングを判断してBeautifulSoupを初期化
        r = requests.get(url)
        content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
        soup = BeautifulSoup(r.content, 'html.parser',
                             from_encoding=content_type_encoding)

        # script,brタグに囲まれた文字を除去
        for tag in soup.find_all('script', 'br'):
            tag.decompose()

        symbols = self.symbols

        for i in range(1, 3):
            # print(str(i))
            if self.css_selector is None:
                css_selector = "#contentsInner > div:nth-child(" + str(
                    i) + ") > div.prt-table > table"
            else:
                css_selector = self.css_selector
            tab = soup.select_one(css_selector)
            # print(tab)

            df = pd.DataFrame(table_to_2d(tab))
            # 1行目を行タイトルに設定
            df.columns = df.iloc[0]
            # df = df.reindex(df.index.drop(0))
            # 1行目を削除
            df.drop(0, inplace=True)
            # 1行目が空白の場合列を削除
            for c_i, col in enumerate(df.columns):
                # print(col.strip())
                if not col.strip():
                    print(col.strip() + '削除')
                    df.drop(df.columns[c_i], axis=1, inplace=True)

            # 1列目にsymbolsの内容を挿入
            df.insert(0, '', symbols[i-1])
            csv_file_name = self.csv_file_name
            df.to_csv(csv_file_name + str(i) + '.csv', sep=',',
                      encoding='utf-8', header=True, index=False)

        return True
