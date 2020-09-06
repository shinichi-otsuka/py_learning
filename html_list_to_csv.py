#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
#import urllib.request
import urllib3
from bs4 import BeautifulSoup
import certifi
import re
import pandas

#技術概要
url = "https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan03.html"
#html = urllib.request.urlopen(url)
# httpsの証明書検証を実行している
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())
r = http.request('GET', url)

soup = BeautifulSoup(r.data, 'html.parser')
soup.find("br").decompose()

symbols = ['S','K']
#delimiter = ","

#table = soup.find_all("table")
for i in range(1,3):
    tab = soup.select_one("#contentsInner > div:nth-child(" + str(i) + ") > div.prt-table > table")
    #tab = soup.select_one("#contentsInner > div:nth-child(1) > div.prt-table > table")
    #print(tab)

    # CSV保存部分
    with open("gijutu" + str(i) + ".csv", "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        rows = tab.find_all("tr")
        #print(rows)
        #break
        for row in rows:
            csvRow = []
            csvRow.append(symbols[i-1])
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text().replace("\r","").replace("\n","").replace("\u3000",""))
#            print(csvRow)
            writer.writerow(csvRow)

