# -*- coding: utf-8 -*-
"""
勤務レポートをLINE通知する.
"""
<<<<<<< HEAD
import os
import requests
=======
import requests
import os
>>>>>>> origin/master
from module import report

URL = os.environ['LINE_URL']
TOKEN = os.environ['LINE_TOKEN']
HEADERS = {'Authorization': 'Bearer '+ TOKEN}


def send_success():
    """
<<<<<<< HEAD
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
=======
    勤務レポート作成成功.
    """
    message = report.TODAY
    payload = {'message': message}
    files = {'imageFile': open('./module/report.png', 'rb')}

    requests.post(URL, headers=HEADERS, params=payload, files=files)


def send_error():
    """
    勤務レポート作成失敗.
    """
    message = '勤務レポートの作成に失敗しました'
    payload = {'message': message}

    requests.post(URL, headers=HEADERS, params=payload)
>>>>>>> origin/master
