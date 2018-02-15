# coding: utf-8
import ConfigParser
import inspect
import time
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import AutomaticToyokoInnReservation, FileGenerationManager, FileLogger

if __name__ == "__main__":
    # コマンドライン引数取得
    CHK_DATE = sys.argv[1]

    # 設定ファイル読込
    settings = ConfigParser.SafeConfigParser()
    settings.read("./CrawlConfig.ini")
    APP_PATH            = settings.get("FILEPATH", "APP_PATH")
    DRIVER_PATH         = settings.get("FILEPATH", "DRIVER_PATH")
    LOG_PATH            = settings.get("FILEPATH", "LOG_PATH")
    LOG_NAME            = settings.get("FILEPATH", "LOG_NAME")
    BASE_URL            = settings.get("URL", "BASE_URL")
    HOTEL_ID            = settings.get("URL", "HOTEL_ID")
    ROOM_TYPE           = settings.get("URL", "ROOM_TYPE")
    LOGIN_ADDRESS       = settings.get("LOGIN", "LOGIN_ADDRESS")
    LOGIN_PASS          = settings.get("LOGIN", "LOGIN_PASS")
    LOGIN_TEL           = settings.get("LOGIN", "LOGIN_TEL")
    TIME_SLEEP          = int(settings.get("CONFIG", "TIME_SLEEP"))
    ENABLE_NOSMOKING    = settings.get("CONFIG", "ENABLE_NOSMOKING")
    ENABLE_SMOKING      = settings.get("CONFIG", "ENABLE_SMOKING")
    CHKIN_VALUE         = settings.get("CONFIG", "CHKIN_VALUE")
    PRTSCR_PATH         = settings.get("SCREENSHOT", "PRTSCR_PATH")
    PRTSCR_WIDTH        = int(settings.get("SCREENSHOT", "PRTSCR_WIDTH"))
    PRTSCR_HEIGHT       = int(settings.get("SCREENSHOT", "PRTSCR_HEIGHT"))
    PRTSCR_MAX_FILE     = int(settings.get("SCREENSHOT", "PRTSCR_MAX_FILE"))

    # ログオブジェクト生成
    FileLogger.logger = FileLogger.FileLogger(LOG_PATH, LOG_NAME)
    FileLogger.logger.log_info("Program Start")
    FileLogger.logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))

    # 禁煙、喫煙文字列
    if ENABLE_NOSMOKING == '1':
        str_smoke = u"禁煙"
    else:
        str_smoke = u"喫煙"

    # スクリーンショット保存パス生成
    if not os.path.exists(PRTSCR_PATH):
        os.makedirs(PRTSCR_PATH)

    FileLogger.logger.log_info(u"エンジン生成")
    options = Options()
    options.binary_location = APP_PATH
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)
    driver.set_window_size(PRTSCR_WIDTH, PRTSCR_HEIGHT)
    count = 0
    while True:
        count += 1
        try:
            r = AutomaticToyokoInnReservation.GetReservation(driver, CHK_DATE, BASE_URL, HOTEL_ID, ROOM_TYPE, LOGIN_ADDRESS, LOGIN_PASS, LOGIN_TEL, ENABLE_NOSMOKING, ENABLE_SMOKING, CHKIN_VALUE)

        except:
            # 処理されていない例外の場合、スクリーンショットを取って終了する
            # YYYYMMDDHHMMSS_[LOG_NAME]_[HOTEL_ID].png
            prtscr_path = u"{0}\\{1}_{2}_{3}.png".format(PRTSCR_PATH, datetime.now().strftime("%Y%m%d%H%M%S"), LOG_NAME, HOTEL_ID)
            sFile = driver.get_screenshot_as_file(prtscr_path)
            # 保存できたらファイルの世代管理
            if sFile:
                FileGenerationManager.ManageGeneration(PRTSCR_PATH, PRTSCR_MAX_FILE, "*.png")
            break

        if r:
            print(u"{0}  {1}  {2}  {3} ………… 予約成功（{4}）".format(CHK_DATE, HOTEL_ID, ROOM_TYPE, str_smoke, count))
            break

        else:
            print(u"{0}  {1}  {2}  {3} ………… 満室（{4}）".format(CHK_DATE, HOTEL_ID, ROOM_TYPE, str_smoke, count))
            FileLogger.logger.log_info(u"{0}秒待った後再実行します".format(TIME_SLEEP))
            time.sleep(TIME_SLEEP)

    driver.quit()
    FileLogger.logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    FileLogger.logger.log_info("Program End")