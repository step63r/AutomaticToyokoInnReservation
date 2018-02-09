# coding: utf-8
import ConfigParser
import inspect
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import AutomaticToyokoInnReservation
from CrawlLogger import Crawl_Logger

if __name__ == "__main__":
    # 設定ファイル読込
    settings = ConfigParser.SafeConfigParser()
    settings.read("./CrawlConfig.ini")
    APP_PATH            = settings.get("FILEPATH", "APP_PATH")
    DRIVER_PATH         = settings.get("FILEPATH", "DRIVER_PATH")
    LOG_PATH            = settings.get("FILEPATH", "LOG_PATH")
    LOG_NAME            = settings.get("FILEPATH", "LOG_NAME")
    TIME_SLEEP          = int(settings.get("CONFIG", "TIME_SLEEP"))

    # ログオブジェクト生成
    Crawl_Logger.create_logger(LOG_PATH, LOG_NAME)
    Crawl_Logger.log_info("Program Start")
    Crawl_Logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))

    Crawl_Logger.log_info(u"エンジン生成")
    options = Options()
    options.binary_location = APP_PATH
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)
    count = 0
    while True:
        count += 1
        r = AutomaticToyokoInnReservation.GetReservation(driver)
        if r:
            print(u"{0} 回目：空室を見つけました！".format(count))
            break
        else:
            print(u"{0} 回目：満室".format(count))
            Crawl_Logger.log_info(u"{0}秒待った後再実行します".format(TIME_SLEEP))
            time.sleep(TIME_SLEEP)

    driver.quit()
    Crawl_Logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    Crawl_Logger.log_info("Program End")