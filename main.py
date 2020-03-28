<<<<<<< HEAD
"""
実行モジュール
"""
import sys
from module import collect
from module import report
from module import line
=======
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
>>>>>>> origin/master


def run():
    """
<<<<<<< HEAD
    実行関数.
    """

    result_collect = collect.collect_controller()
    if result_collect is True:

        ins = report.CreateWorkReport()
        result_create_report = ins.create()
        if result_create_report is True:
            line.send_success()
            sys.exit()
        else:
            err_msg = result_create_report
    else:
        err_msg = result_collect
    line.send_error(err_msg)


if __name__ == "__main__":
    run()
=======
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
>>>>>>> origin/master
