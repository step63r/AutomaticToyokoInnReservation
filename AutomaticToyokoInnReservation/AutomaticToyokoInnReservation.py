# coding: utf-8
import sys
import inspect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import FileLogger, XPathConfig

STR_VALIDATE = u"ご予約ありがとうございました。"

def SearchRoom(driver, xpath):
    ret = False
    try:
        driver.find_elements_by_xpath(xpath)[0].click()

    except IndexError:
        ret = False

    return ret

def GetReservation(driver, CHK_DATE, BASE_URL, HOTEL_ID, ROOM_TYPE, LOGIN_ADDRESS, LOGIN_PASS, LOGIN_TEL, ENABLE_NOSMOKING, ENABLE_SMOKING, PRIORITY, CHKIN_VALUE):
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
    except IndexError:
        pass

    FileLogger.logger.log_info(u"詳細ページへ移動中")
    # 詳細ページへ
    driver.get("{0}search/detail//{1}".format(BASE_URL, HOTEL_ID))
    FileLogger.logger.log_info(u"予約ページへ移動中")
    # 予約ページへ
    driver.get("{0}search/reserve/room?chckn_date={1}&room_type={2}".format(BASE_URL, CHK_DATE, ROOM_TYPE))
    
    if ENABLE_NOSMOKING == '0' and ENABLE_SMOKING == '0':
        FileLogger.logger.log_error(u"禁煙・喫煙の選択がありません")
        raise ValueError(u"禁煙・喫煙の選択がありません")    
    
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
    
    # 正しく予約できたことを確認
    try:
        str_chk = driver.find_element_by_xpath(XPathConfig.XPATH_CHK_VALIDATE)[0].text == STR_VALIDATE

        if not str_chk == STR_VALIDATE:
            # 要素はあるが文字が違う
            FileLogger.logger.log_info(u"Webページの文字列：{0}".format(str_chk))
            FileLogger.logger.log_info(u"正常な文字列：{0}".format(STR_VALIDATE))
            FileLogger.logger.log_warning(u"空室を見つけましたが予約できませんでした")
            ret = False

    except IndexError:
        # 要素がない
        FileLogger.logger.log_warning(u"空室を見つけましたが予約できませんでした")
        ret = False

    FileLogger.logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    return ret