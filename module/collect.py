# -*- coding: utf-8 -*-
"""
勤怠管理サイトからCSVをダウンロード.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

from . import log
import time
import os

# Headlessモード定義
OPTS = Options()
OPTS.add_argument('--headless')
OPTS.add_argument('--no-sandbox')
OPTS.add_argument('--disable-dev-shm-usage')
DRV = webdriver.Chrome(executable_path='/app/lib/chromedriver', options=OPTS)


def scraping():
    """
    ログインする.
    成功した場合、ダウンロード画面へ遷移する
    """

    URL = os.environ['WORK_LOGIN_URL']
    ID = os.environ['WORK_ID']
    AUTH = os.environ['WORK_AUTH']
    PASSWORD = os.environ['WORK_PASSWORD']

    try:
        DRV.get(URL)
    except Exception:
        log.error('start_scraping: Not Found login page')
        return False

    try:
        DRV.find_element_by_id('contractId').send_keys(ID)
        DRV.find_element_by_id('authId').send_keys(AUTH)
        DRV.find_element_by_id('password').send_keys(PASSWORD)
    except Exception:
        log.error('start_scraping: Not Found login element')
        return False

    # ログイン情報入力中にボタンクリック防止
    time.sleep(2)

    try:
        DRV.find_element_by_tag_name("button").click()
    except Exception:
        log.error('start_scraping: login error')
        return False

    return transition_to_download(DRV)


def transition_to_download(DRV):
    """
    ダウンロード画面へ遷移する.

    param:
       drv webdriver
    """

    URL = os.environ['WORK_DW_URL']

    try:
        DRV.get(URL)
    except Exception:
        log.error('transition_to_download: Not Found work-report page')
        return False

    try:
        DRV.execute_script("loadExportDialogForAttendance('01')")
    except Exception:
        log.error('transition_to_download: Not Found download modal')
        return False

    # モーダル表示中にボタンクリック防止
    time.sleep(3)

    try:
        DRV.execute_script('downloadLayout()')
    except Exception:
        log.error('transition_to_download: download click error')
        return False

    return True


def download_csv():
    """
    CSVをダウンロードする.

    param:
        drv webdriver
    """

    if scraping():
        DRV.command_executor._commands["send_command"] = \
            ("POST", '/session/$sessionId/chromium/send_command')

        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': 'module'
            }
        }

        DRV.execute("send_command", params)

        # CSVダウンロード中にclose防止
        time.sleep(5)
    else:
        log.error('download_csv: download error')
        return False

    DRV.close()
    DRV.quit()

    log.info('download_csv: download success')
    return True