# -*- coding: utf-8 -*-
"""
勤務レポートをLINE通知する.
"""
import os
import requests
from module import report

URL = os.environ['LINE_URL']
TOKEN = os.environ['LINE_TOKEN']
HEADERS = {'Authorization': 'Bearer '+ TOKEN}


def send_success():
    """
    勤務レポート作成成功パターン.
    """
    requests.post(URL, headers=HEADERS,
                  params={'message': report.TODAY},
                  files={'imageFile': open('./module/report.png', 'rb')})
    os.remove('./module/report.png')


def send_error(err_msg):
    """
    勤務レポート作成失敗パターン.

    @param:
        err_msg エラーメッセージ
    """
    requests.post(URL, headers=HEADERS, params={'message': err_msg})
