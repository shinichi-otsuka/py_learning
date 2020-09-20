import sys
import argparse
import csv
import datetime
import filecmp
from difflib import HtmlDiff

class diff_2file():

#    def __init__(self, f1=None, f2=None):
#        self._f1 = f1
#        self._f2 = f2

#   @property
#    def f1(self):
#        return self._f1

#    @f1.setter
#    def f1(self, f1):
#        self._f1 = f1

#    @property
#    def f2(self):
#        return self._f2

#    @f2.setter
#    def f2(self, f2):
#        self._f2 = f2

#    @property
#    def outfile(self):
#        dtm_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#        self.__outfile = 'diff_csv_' + dtm_str + '.html'
#        return self.__outfile

    def diffOutHtml(self, f1, f2, outfile = 'diff_csv_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html', sorting_column = 0):
        # ファイルに差異があればHTML形式で出力
        df_exists = not filecmp.cmp(f1, f2)
        if df_exists:        
            df_html = HtmlDiff()

            with open(f1, 'r') as t1, open(f2, 'r') as t2:
                fileone = t1.readlines()
                filetwo = t2.readlines()

            #print(diff_str)
            with open(outfile, 'w') as outFile:
                outFile.writelines(df_html.make_file(fileone,filetwo,f1,f2))
        
        return df_exists

    def diffOutCsv(self, f1, f2, outfile, sorting_column):
    # 同じ内容が２行あると差分判定できないため不採用
        with open(f1, 'r') as t1, open(f2, 'r') as t2:
            fileone = t1.readlines()
            filetwo = t2.readlines()

        with open(outfile, 'w') as outFile:
            for line in filetwo:
                if line not in fileone:
                    outFile.write(line)

#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()

    #parser.add_argument('infile', nargs=2, type=argparse.FileType('r'))
    #parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
#    parser.add_argument('infile', nargs=2, type=str)
#    parser.add_argument('outfile', nargs='?', type=str, default='diff_csv_' + dtm_str + '.html')
#    parser.add_argument('-sc', '--sorting-column', nargs='?', type=int, default=0)

#    args = parser.parse_args()

#    sys.exit(int(main(*args.infile, args.outfile, args.sorting_column))) 