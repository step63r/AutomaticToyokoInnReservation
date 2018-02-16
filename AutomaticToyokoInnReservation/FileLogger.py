# coding: utf-8
import logging
import logging.handlers
import os
from datetime import datetime

# ログオブジェクト
logger = None

class FileLogger(object):
    """
    概略：
        - ログファイルを生成する
    引数：
        - path [str] ログ出力先パス
        - log_name [str] ログファイル名（YYYYMMDDHHMMSS_hogehoge.log）
    戻り値：
        - ログファイルが生成される。
        - マルチスレッド非対応
    """
    filelogger = None

    def __init__(self, path, log_name, max_bytes=1048576, backup_count=20, log_level=20):
        """
        概略：
            - ログオブジェクトを生成する
        引数：
            - path [str] ログファイルパス
            - log_name [str] ログファイル名
            - max_bytes [int] 1ファイルあたりの最大サイズ（初期値：1MB）
            - backup_count [int] 最大ローテーション数（初期値：20）
            - log_level [int] 出力レベル（初期値：INFO）
        """
        if not os.path.exists(path):
            os.makedirs(path)
        self.filelogger = logging.getLogger(__name__)
        self.filelogger.setLevel(log_level)
        handler = logging.handlers.RotatingFileHandler(
            "{0}/{1}_{2}.log".format(path, datetime.now().strftime("%Y%m%d%H%M%S"), log_name),
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname).1s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.filelogger.addHandler(handler)

    def log_debug(self, str):
        """
        概略：
            - DEBUGレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        self.filelogger.debug(str)

    def log_info(self, str):
        """
        概略：
            - INFOレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        self.filelogger.info(str)

    def log_warning(self, str):
        """
        概略：
            - WARNINGレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        self.filelogger.warning(str)

    def log_error(self, str):
        """
        概略：
            - ERRORレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        self.filelogger.error(str)
    
    def log_critical(self, str):
        """
        概略：
            - CRITICALレベルのログを出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する。
        """
        self.filelogger.critical(str)

    def log_exception(self, str):
        """
        概略：
            - 例外情報を出力する
        引数：
            - str [str] 出力メッセージ
            - fileloggerが生成されている
        戻り値：
            - ログを出力する
        """
        self.filelogger.exception(str)