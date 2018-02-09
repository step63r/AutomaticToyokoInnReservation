# coding: utf-8
import sys
import ConfigParser
import inspect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from CrawlLogger import Crawl_Logger

def GetReservation(driver):
    Crawl_Logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    ret = True

    # 設定ファイル読込
    settings = ConfigParser.SafeConfigParser()
    settings.read("./CrawlConfig.ini")
    BASE_URL            = settings.get("URL", "BASE_URL")
    HOTEL_ID            = settings.get("URL", "HOTEL_ID")
    ROOM_TYPE           = settings.get("URL", "ROOM_TYPE")
    CHK_DATE            = settings.get("URL", "CHK_DATE")
    LOGIN_ADDRESS       = settings.get("LOGIN", "LOGIN_ADDRESS")
    LOGIN_PASS          = settings.get("LOGIN", "LOGIN_PASS")
    LOGIN_TEL           = settings.get("LOGIN", "LOGIN_TEL")
    ENABLE_NOSMOKING    = settings.get("CONFIG", "ENABLE_NOSMOKING")
    ENABLE_SMOKING      = settings.get("CONFIG", "ENABLE_SMOKING")
    CHKIN_VALUE         = settings.get("CONFIG", "CHKIN_VALUE")
    XPATH_FAVORITE      = settings.get("XPATH", "XPATH_FAVORITE")
    XPATH_FORM_ADDRESS  = settings.get("XPATH", "XPATH_FORM_ADDRESS")
    XPATH_PASS          = settings.get("XPATH", "XPATH_PASS")
    XPATH_LOGINBTN      = settings.get("XPATH", "XPATH_LOGINBTN")
    XPATH_NOSMOKING     = settings.get("XPATH", "XPATH_NOSMOKING")
    XPATH_SMOKING       = settings.get("XPATH", "XPATH_SMOKING")
    XPATH_TEL           = settings.get("XPATH", "XPATH_TEL")
    XPATH_CHKINTIME     = settings.get("XPATH", "XPATH_CHKINTIME")
    XPATH_CONFIRM       = settings.get("XPATH", "XPATH_CONFIRM")
    XPATH_OK            = settings.get("XPATH", "XPATH_OK")
    
    Crawl_Logger.log_info(u"サイトへアクセス中")
    # アクセス
    driver.get(BASE_URL)
    
    Crawl_Logger.log_info(u"お気に入りへ移動中")
    # 「お気に入りリスト」をクリック
    driver.find_elements_by_xpath(XPATH_FAVORITE)[0].click()
    Crawl_Logger.log_info(u"ログイン中")
    # ログイン処理
    try:
        driver.find_elements_by_xpath(XPATH_FORM_ADDRESS)[0].send_keys(LOGIN_ADDRESS)
        driver.find_elements_by_xpath(XPATH_PASS)[0].send_keys(LOGIN_PASS)
        driver.find_elements_by_xpath(XPATH_LOGINBTN)[0].click()
    except:
        pass

    Crawl_Logger.log_info(u"詳細ページへ移動中")
    # 詳細ページへ
    driver.get("{0}search/detail//{1}".format(BASE_URL, HOTEL_ID))
    Crawl_Logger.log_info(u"予約ページへ移動中")
    # 予約ページへ
    driver.get("https://www.toyoko-inn.com/search/reserve/room?chckn_date={0}&room_type={1}".format(CHK_DATE, ROOM_TYPE))
    
    if ENABLE_NOSMOKING == '1':
        Crawl_Logger.log_info(u"禁煙ルームを検索中")
        try:
            driver.find_elements_by_xpath(XPATH_NOSMOKING)[0].click()
        except:
            # エレメントがない場合、予約不可
            Crawl_Logger.log_warning(u"{0}の禁煙ルームは満室でした".format(CHK_DATE))
            ret = False
            
    elif ENABLE_SMOKING == '1':
        Crawl_Logger.log_info(u"喫煙ルームを検索中")
        try:
            driver.find_elements_by_xpath(XPATH_SMOKING)[0].click()
        except:
            # エレメントがない場合、予約不可
            Crawl_Logger.log_warning(u"{0}の喫煙ルームは満室でした".format(CHK_DATE))
            ret = False
    else:
        Crawl_Logger.log_error(u"禁煙・喫煙の選択がありません")
        ret = False
    
    if ret:
        # 電話番号入力
        driver.find_elements_by_xpath(XPATH_TEL)[0].send_keys(LOGIN_TEL)
        # チェックイン予定時刻
        chktime_element = driver.find_elements_by_xpath(XPATH_CHKINTIME)[0]
        chktime_select_element = Select(chktime_element)
        chktime_select_element.select_by_value(CHKIN_VALUE)
        # 確認ボタン押下
        driver.find_elements_by_xpath(XPATH_CONFIRM)[0].click()
        # 確定ボタン押下
        driver.find_elements_by_xpath(XPATH_OK)[0].click()
    
    Crawl_Logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    return ret