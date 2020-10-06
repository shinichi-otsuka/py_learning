import os
import datetime
import traceback
from html_table_to_csv import htmltable_scraping
from diff_csv import diff_2file
from merge_csvfiles import merge_csvfiles
from cleansing_csv import clg_csv
import slack

txt_message = ''

try:
    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    html_scr = htmltable_scraping()

    html_scr.url = 'https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan03.html'
    html_scr.csv_file_name = 'gijutu'
    html_scr.html_to_csv()

    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    mrg = merge_csvfiles(file_name='gijutu')
    mrg.merge()
    # mrg = merge_csvfiles()
    # mrg.csv_file_name = 'gijutu'

    # 先頭末尾のスペース改行文字を除去、文中の改行文字は全角￥ｒ￥ｎに変換
    clg_c = clg_csv()
    clg_c.replace_str_csv()

    # 比較元ファイル存在確認
    if os.path.exists('pre_gijutu.csv'):
        # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
        df_2f = diff_2file()
        if df_2f.diffOutHtml('pre_gijutu.csv', 'clg_gijutu.csv'):
            # preファイルをbk+システム日時ファイル名で保存
            dt = datetime.datetime.fromtimestamp(
                os.path.getctime('pre_gijutu.csv'))
            os.rename('pre_gijutu.csv', 'bk_gijutu_' +
                      dt.strftime('%Y%m%d%H%M%S') + '.csv')
            os.rename('clg_gijutu.csv', 'pre_gijutu.csv')
            print('差異あり_技術概要')
            txt_message += '差異あり_技術概要\r\n'
        else:
            print('差異なし_技術概要')
            txt_message += '差異なし_技術概要\r\n'
    else:
        # 比較元ファイルがない場合、カレントファイルをpreファイルとして保存
        os.rename('clg_gijutu.csv', 'pre_gijutu.csv')
        print('差異比較ファイルなし_技術概要')
        txt_message += '差異比較ファイルなし_技術概要\r\n'

    # 医療機関一覧
    html_scr.url = 'https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan02.html'
    html_scr.csv_file_name = 'iryokikan'
    html_scr.html_to_csv()

    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    mrg = merge_csvfiles(file_name='iryokikan')
    mrg.merge()

    # 先頭末尾のスペース改行文字を除去、文中の改行文字は全角￥ｒ￥ｎに変換
    clg_c = clg_csv()
    clg_c.replace_str_csv('mrg_iryokikan.csv', 'clg_iryokikan.csv')

    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    df_2f = diff_2file()

    # 比較元ファイル存在確認
    if os.path.exists('pre_iryokikan.csv'):
        if df_2f.diffOutHtml('pre_iryokikan.csv', 'clg_iryokikan.csv'):
            dt = datetime.datetime.fromtimestamp(
                os.path.getctime('pre_iryokikan.csv'))
            os.rename('pre_iryokikan.csv', 'bk_iryokikan_' +
                      dt.strftime('%Y%m%d%H%M%S') + '.csv')
            os.rename('clg_iryokikan.csv', 'pre_iryokikan.csv')
            print('差異あり_医療機関一覧')
            txt_message += '差異あり_医療機関一覧\r\n'
        else:
            print('差異なし_医療機関一覧')
            txt_message += '差異なし_医療機関一覧\r\n'
    else:
        # 比較元ファイルがない場合、カレントファイルをpreファイルとして保存
        os.rename('clg_iryokikan.csv', 'pre_iryokikan.csv')
        print('差異比較ファイルなし_医療機関一覧')
        txt_message += '差異比較ファイルなし_医療機関一覧\r\n'

except Exception:
    txt_message += traceback.format_exc()
    print(traceback.format_exc())
finally:
    # slackチャンネルへ投稿
    wh = slack.webhook()
    wh.url = 'https://hooks.slack.com/services/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'
    wh.username = 'robot_senshiniryo'
    wh.text = txt_message

    wh.post_json()
