import os
import pandas as pd
import glob


class merge_csvfiles:
    def __init__(self, cur_path=os.path.dirname(__file__), file_name=None):
        self.__cur_path = cur_path
        self.__file_name = file_name

    def merge(self):
        if self.__file_name is None:
            raise Exception('file_name is None')
        # パスで指定したファイルの一覧をリスト形式で取得. （ここでは一階層下のtestファイル以下）
        csv_files = glob.glob(self.__cur_path + '/' +
                              self.__file_name + '*.csv')

        # 読み込むファイルのリストを表示
        for a in csv_files:
            print(a)

        # csvファイルの中身を追加していくリストを用意
        data_list = []

        # 読み込むファイルのリストを走査
        for file in csv_files:
            data_list.append(pd.read_csv(file))

        # リストを全て行方向に結合
        # axis=0:行方向に結合（sortすると列順が崩れるためしない）
        df = pd.concat(data_list, axis=0, sort=False)

        # print(df)

        df.to_csv(self.__cur_path + '/' +
                  'mrg_' + self.__file_name + '.csv', index=False)
