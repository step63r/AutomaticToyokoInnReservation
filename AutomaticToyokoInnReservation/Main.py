# coding: utf-8
import ConfigParser
import inspect
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import AutomaticToyokoInnReservation
import FileLogger

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
    TIME_SLEEP          = int(settings.get("CONFIG", "TIME_SLEEP"))

    # ログオブジェクト生成
    FileLogger.logger = FileLogger.FileLogger(LOG_PATH, LOG_NAME)
    FileLogger.logger.log_info("Program Start")
    FileLogger.logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))

    FileLogger.logger.log_info(u"エンジン生成")
    options = Options()
    options.binary_location = APP_PATH
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)
    count = 0
    while True:
        count += 1
        r = AutomaticToyokoInnReservation.GetReservation(driver, CHK_DATE)
        if r:
            print(u"{0} 回目：空室を見つけました！".format(count))
            break
        else:
            print(u"{0} 回目：満室".format(count))
            FileLogger.logger.log_info(u"{0}秒待った後再実行します".format(TIME_SLEEP))
            time.sleep(TIME_SLEEP)

    driver.quit()
    FileLogger.logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    FileLogger.logger.log_info("Program End")