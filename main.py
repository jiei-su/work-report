# -*- coding: utf-8 -*-
"""
実行モジュール
"""
from module import collect
from module import report
from module import line
import glob
import os


def search_csv_from_dir():
    """
    CSVファイルを検索する.
    CSVダウンロードから本関数がコールされるまでに
    CSVが削除されることを考慮

    return:
      csv CSVファイル名
    """

    try:
        for file in glob.glob('./module/*.csv'):
            csv = file
    except FileNotFoundError:
        return None
    else:
        return csv


def run():
    """
    プログラム実行関数.
    """

    download = collect.download_csv()
    search_csv = search_csv_from_dir()
    if download and search_csv is not None:
        ins = report.CreateWorkReport(search_csv)
        ins.create_report()

        line.send_success()
    else:
        line.send_error()

    os.remove(search_csv)

if __name__ == "__main__":
    run()