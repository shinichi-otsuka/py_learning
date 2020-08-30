#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip install tabula-py
import sys
import tabula
#import pandas as pd
from pathlib import Path
import datetime
now = datetime.datetime.now()
now = now.strftime("%y%m%d%H%M%S")


def main():
    
    tabula.convert_into(path_pdf, file_name + '_'+ now + '.csv', pages="all", output_format="csv")

if __name__ == '__main__':
    args = sys.argv
    path_pdf = args[1]
    
    file_name = Path(path_pdf).stem #ファイルパスから、拡張子抜きファイル名を取得
    
    main()