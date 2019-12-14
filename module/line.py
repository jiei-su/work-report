# -*- coding: utf-8 -*-
"""
勤務レポートをLINE通知する.
"""
import requests
import os
from module import report

URL = os.environ['LINE_URL']
TOKEN = os.environ['LINE_TOKEN']
HEADERS = {'Authorization': 'Bearer '+ TOKEN}


def send_success():
    """
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