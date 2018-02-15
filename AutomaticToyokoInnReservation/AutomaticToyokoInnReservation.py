# coding: utf-8
import sys
import inspect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import FileLogger, XPathConfig

def GetReservation(driver, CHK_DATE, BASE_URL, HOTEL_ID, ROOM_TYPE, LOGIN_ADDRESS, LOGIN_PASS, LOGIN_TEL, ENABLE_NOSMOKING, ENABLE_SMOKING, CHKIN_VALUE):
    FileLogger.logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    ret = True
    
    FileLogger.logger.log_info(u"サイトへアクセス中")
    # アクセス
    driver.get(BASE_URL)
    
    FileLogger.logger.log_info(u"お気に入りへ移動中")
    # 「お気に入りリスト」をクリック
    driver.find_elements_by_xpath(XPathConfig.XPATH_FAVORITE)[0].click()
    FileLogger.logger.log_info(u"ログイン中")
    # ログイン処理
    try:
        driver.find_elements_by_xpath(XPathConfig.XPATH_FORM_ADDRESS)[0].send_keys(LOGIN_ADDRESS)
        driver.find_elements_by_xpath(XPathConfig.XPATH_PASS)[0].send_keys(LOGIN_PASS)
        driver.find_elements_by_xpath(XPathConfig.XPATH_LOGINBTN)[0].click()
    except:
        pass

    FileLogger.logger.log_info(u"詳細ページへ移動中")
    # 詳細ページへ
    driver.get("{0}search/detail//{1}".format(BASE_URL, HOTEL_ID))
    FileLogger.logger.log_info(u"予約ページへ移動中")
    # 予約ページへ
    driver.get("{0}search/reserve/room?chckn_date={1}&room_type={2}".format(BASE_URL, CHK_DATE, ROOM_TYPE))
    
    if ENABLE_NOSMOKING == '1':
        FileLogger.logger.log_info(u"禁煙ルームを検索中")
        try:
            driver.find_elements_by_xpath(XPathConfig.XPATH_NOSMOKING)[0].click()
        except:
            # エレメントがない場合、予約不可
            FileLogger.logger.log_warning(u"{0}の禁煙ルームは満室でした".format(CHK_DATE))
            ret = False
            
    elif ENABLE_SMOKING == '1':
        FileLogger.logger.log_info(u"喫煙ルームを検索中")
        try:
            driver.find_elements_by_xpath(XPathConfig.XPATH_SMOKING)[0].click()
        except:
            # エレメントがない場合、予約不可
            FileLogger.logger.log_warning(u"{0}の喫煙ルームは満室でした".format(CHK_DATE))
            ret = False
    else:
        FileLogger.logger.log_error(u"禁煙・喫煙の選択がありません")
        ret = False
    
    if ret:
        # 電話番号入力
        driver.find_elements_by_xpath(XPathConfig.XPATH_TEL)[0].send_keys(LOGIN_TEL)
        # チェックイン予定時刻
        chktime_element = driver.find_elements_by_xpath(XPathConfig.XPATH_CHKINTIME)[0]
        chktime_select_element = Select(chktime_element)
        chktime_select_element.select_by_value(CHKIN_VALUE)
        # 確認ボタン押下
        driver.find_elements_by_xpath(XPathConfig.XPATH_CONFIRM)[0].click()
        # 確定ボタン押下
        driver.find_elements_by_xpath(XPathConfig.XPATH_OK)[0].click()
    
    FileLogger.logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    return ret