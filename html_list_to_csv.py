#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas

#技術概要
url = "https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan03.html"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
soup.find("br").decompose()

symbols = ['S','K']
delimiter = ","

#table = soup.find_all("table")
for i in range(1,2):
    tab = soup.select_one("#contentsInner > div:nth-child(" + i + ") > div.prt-table > table")
    #tab = soup.select_one("#contentsInner > div:nth-child(1) > div.prt-table > table")
    print(tab)
    break

    # CSV保存部分
    with open("gijutu" + i  +  ".csv", "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        rows = tab.find_all("tr")
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                
                csvRow.append(symbols(i) + delimiter + cell.get_text().replace("\r","").replace("\n","").replace("\u3000",""))
            print(csvRow)
            writer.writerow(csvRow)


