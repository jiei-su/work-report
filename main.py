"""
実行モジュール
"""
import sys
from module import collect
from module import report
from module import line


def run():
    """
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
