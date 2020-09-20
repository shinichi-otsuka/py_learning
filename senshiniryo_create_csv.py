import traceback
from html_table_to_csv import htmltable_scraping
from diff_csv import diff_2file
from merge_csvfiles import merge_csvfiles

try:
    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    #html_scr = htmltable_scraping()

    #html_scr.url = 'https://www.mhlw.go.jp/topics/bukyoku/isei/sensiniryo/kikan03.html'
    #html_scr.csv_file_name = 'gijutu'
    #html_scr.html_to_csv()

    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    mrg = merge_csvfiles(file_name='gijutu')
    #mrg = merge_csvfiles()
    #mrg.csv_file_name = 'gijutu'
    mrg.merge()

    # インスタンス初期化（実施しないとメソッド呼び出しで引数がずれる）
    df_2f = diff_2file()

    if df_2f.diffOutHtml('gijutu1.csv', 'gijutu1_same.csv'):
        print('差異あり')
    else:
        print('差異なし')

    if df_2f.diffOutHtml('gijutu1.csv','gijutu3.csv'):
        print('差異あり')
    else:
        print('差異なし')
except Exception as ex:
        print(traceback.format_exc())
finally:
    pass


