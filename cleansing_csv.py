import pandas as pd


class clg_csv():

    def replace_str_csv(self, infile='mrg_gijutu.csv', outfile='clg_gijutu.csv'):
        df = pd.read_csv(infile, dtype='object', encoding='utf-8')
        # 先頭スペースは除去する
        df = df.replace('＾\r?\n?[　 ]', '', regex=True)
        # 末尾スペースと\r\nは除去する
        df = df.replace('\r?\n?[　 ]{0,2}$', '', regex=True)
        # \r\nを全角文字￥ｒ￥ｎに置き換える
        df = df.replace('\r\n', '￥ｒ￥ｎ', regex=True)
        # \nを全角文字￥ｎに置き換える
        df = df.replace('\n', '￥ｎ', regex=True)
        # df = df.replace({'技術の概要': {'\n': '￥ｎ'}}, regex=True)
        df.to_csv(outfile, sep=',',
                  encoding='utf-8', header=True, index=False)
