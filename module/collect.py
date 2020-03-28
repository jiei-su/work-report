"""
勤怠管理サイトからCSVをダウンロード.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Headlessモード定義
OPTS = Options()
OPTS.add_argument('--headless')
OPTS.add_argument('--no-sandbox')
OPTS.add_argument('--disable-dev-shm-usage')
DRV = webdriver.Chrome(executable_path='lib/chromedriver', options=OPTS)

ERR_MSG = {
    'NOT_FOUND_LOGIN': 'ログインURLが見つかりませんでした',
    'NOT_FOUND_DOWNLOAD': 'ダウンロード画面が見つかりませんでした',
    'LOGIN_FAIL': 'ログイン出来ませんでした',
    'GET_FAIL': '取得に失敗しました',
}


def login():
    """
    ログインする.

    @retrun:
        True ログイン成功
    @raise:
        NOT_FOUND_LOGIN エラーメッセージ
        LOGIN_FAIL エラーメッセージ
        GET_FAIL エラーメッセージ
    """
    login_url = os.environ['WORK_LOGIN_URL']
    login_id = os.environ['WORK_ID']
    login_auth = os.environ['WORK_AUTH']
    login_password = os.environ['WORK_PASSWORD']

    try:
        DRV.get(login_url)
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['NOT_FOUND_LOGIN']

    try:
        DRV.find_element_by_id('contractId').send_keys(login_id)
        DRV.find_element_by_id('authId').send_keys(login_auth)
        DRV.find_element_by_id('password').send_keys(login_password)
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['LOGIN_FAIL']

    # ログイン情報入力中にボタンクリック防止
    time.sleep(2)

    try:
        DRV.find_element_by_tag_name("button").click()
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['GET_FAIL']

    return True


def transition_to_download():
    """
    ダウンロード画面へ遷移する.

    @retrun:
        True 遷移成功
    @raise:
        NOT_FOUND_DOWNLOAD エラーメッセージ
        GET_FAIL エラーメッセージ
    """
    download_url = os.environ['WORK_DW_URL']

    try:
        DRV.get(download_url)
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['NOT_FOUND_DOWNLOAD']

    try:
        DRV.execute_script("loadExportDialogForAttendance('01')")
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['GET_FAIL']

    # モーダル表示中にボタンクリック防止
    time.sleep(3)

    try:
        DRV.execute_script('downloadLayout()')
    except Exception:
        # pylint: Catching too general exception Exception
        return ERR_MSG['GET_FAIL']

    return True

def close_driver():
    """
    ドライバーを閉じる.
    """
    DRV.close()
    DRV.quit()

def collect_controller():
    """
    勤務情報を収集する.

    @retrun:
        True 収集成功
    @raise:
        result_to_download エラーメッセージ
        result_login エラーメッセージ
    """
    result_login = login()
    if result_login is True:
        result_to_download = transition_to_download()

        if result_to_download is True:
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
            close_driver()
            return result_to_download
    else:
        close_driver()
        return result_login

    close_driver()
    return True
