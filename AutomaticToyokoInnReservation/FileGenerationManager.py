# coding: utf-8
import glob
import os
import inspect
import FileLogger

def ManageGeneration(dir_path, count_alive, source_glob = ""):
    """
    概略：
        - ファイル作成日時が古いものから順に削除し一定のファイル数を保つ

    引数：
        - dir_path [str] 対象ディレクトリ
        - count_alive [int] 残すファイル数
        - source_glob [str] 対象ファイル形式（例：*.csv）（初期値：空文字）
    """
    FileLogger.logger.log_info("Process Start {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    # ディレクトリがなければ何もしない
    if not os.path.exists(dir_path):
        return

    # カウンタ
    count = 1;
    files = glob.glob("{0}/{1}".format(dir_path, source_glob))
    # 作成日時の降順に並び替え
    files.sort(cmp=lambda x, y: int(os.path.getctime(x) - os.path.getctime(y)), reverse = True)
    
    for oneFile in files:
        if count > count_alive:
            os.remove(oneFile)
        count += 1;

    FileLogger.logger.log_info("Process End {0}.{1}".format(__name__, inspect.getframeinfo(inspect.currentframe())[2]))
    return