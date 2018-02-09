# coding: utf-8
import logging
import logging.handlers
import os
from datetime import datetime

class Crawl_Logger(object):
    """
    概略：
        - ログファイルを生成する
    引数：
        - path [str] ログ出力先パス
        - log_name [str] ログファイル名（YYYYMMDDHHMMSS_hogehoge.log）
    戻り値：
        - ログファイルが生成される。
        - ファイルは最大1MBまで追記され、それを超えるごとに "hogehoge.log.1" のようなファイルに退避される。
        - 退避ファイルは最大20ファイルまで保持され、それ以上は古いものから上書きされる。
        - マルチスレッド非対応
    """
    filelogger = None

    @classmethod
    def create_logger(cls, path, log_name):
        if not os.path.exists(path):
            os.makedirs(path)
        cls.filelogger = logging.getLogger(__name__)
        cls.filelogger.setLevel(logging.INFO)
        #handler = logging.FileHandler("{0}/{1}_FCTIPrediction.log".format(path, datetime.now().strftime("%Y%m%d%H%M%S")))
        handler = logging.handlers.RotatingFileHandler(
            "{0}/{1}_{2}.log".format(path, datetime.now().strftime("%Y%m%d%H%M%S"), log_name),
            maxBytes=1048576,
            backupCount=20
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname).1s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        cls.filelogger.addHandler(handler)

    @classmethod
    def log_info(cls, str):
        """
        概略：
            - INFOレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        cls.filelogger.info(str)

    @classmethod
    def log_warning(cls, str):
        """
        概略：
            - WARNINGレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        cls.filelogger.warning(str)

    @classmethod
    def log_error(cls, str):
        """
        概略：
            - ERRORレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        cls.filelogger.error(str)
    
    @classmethod
    def log_critical(cls, str):
        """
        概略：
            - CRITICALレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        cls.filelogger.critical(str)