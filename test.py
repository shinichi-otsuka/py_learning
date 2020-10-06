# import pandas as pd
#
# dfの列並び替え
# df = pd.read_csv('pre_gijutu.csv', encoding='utf_8')
# print(df.columns)
# df = df[['Unnamed: 0', '番号', 'jRCT登録ID番号https://jrct.niph.go.jp',
#          '先進医療技術名', '適応症', '技術の概要']]
# df.to_csv('pre_gijutu_sort.csv', index=False)

# from merge_csvfiles import merge_csvfiles
# from cleansing_csv import clg_csv

# # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
# mrg = merge_csvfiles(file_name='iryokikan')
# mrg.merge()

# # 先頭末尾のスペース改行文字を除去、文中の改行文字は全角￥ｒ￥ｎに変換
# clg_c = clg_csv()
# clg_c.replace_str_csv('mrg_iryokikan.csv', 'clg_iryokikan.csv')


import slack

# slackチャンネルへ投稿
wh = slack.webhook()
wh.url = 'https://hooks.slack.com/services/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'
wh.username = 'robot_senshiniryo'
wh.text = 'test\r\n2gyo'

wh.post_json()
