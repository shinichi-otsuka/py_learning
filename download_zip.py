#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import zipfile

from download import download
from bs4 import BeautifulSoup

BASE_URL = u"https://kouseikyoku.mhlw.go.jp"
EXTENSION = u".zip"

urls = [
    u"https://kouseikyoku.mhlw.go.jp/tohoku/gyomu/gyomu/hoken_kikan/itiran.html",
    u"https://kouseikyoku.mhlw.go.jp/tokaihokuriku/gyomu/gyomu/hoken_kikan/shitei.html",
]

def zip_extract(filename):
    """ファイル名を指定して zip ファイルをカレントディレクトリに展開する
    """
    target_directory = '.'
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target_directory)

for url in urls:

    download_urls = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    links = soup.findAll('a')

    # URLの抽出
    for link in links:

        href = link.get('href')
        
        #print('all:'+href) #debug1

        if href and EXTENSION in href.lower():
            # print(href)
            download_urls.append(href)

    # ファイルのダウンロード（ひとまず30件に制限）
    for download_url in download_urls[:30]:

        # 一秒スリープ
        time.sleep(1)

        file_name = download_url.split("/")[-1]
        # print(file_name)

        if BASE_URL not in download_url:
            download_url = BASE_URL + download_url
            print(download_url)
        
        
        download(download_url, './' + file_name)
        #r = requests.get(url, stream=True)

        # ファイルの保存
        #if r.status_code == 200:
        #    with open(file_name, 'wb') as f:
        #        for chunk in r.iter_content(chunk_size=1024):
        #            if chunk:
        #                f.write(chunk)
        #                f.flush()
        
        #TODO:フォルダ、ファイル名が文字化けする
        #zip_extract(file_name)

