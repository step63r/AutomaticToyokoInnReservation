# 東横イン自動予約スクリプト
## 概要
設定した条件で東横イン公式HPをクロールして空き部屋があれば予約するスクリプトです。

## 動作環境
* Windows 7 Professional 以上
* Python 2.7.13 :: Anaconda 4.3.1

## 必要なもの
* 上記を満たす環境（主にAnacondaのインストール）
* Google Chrome
* ChromeDriver
* selenium（Python）

## Pythonセットアップ
Anacondaをインストール後、コマンドプロンプトで以下のコマンドを実行して下さい。
```
pip install selenium
```

## iniファイルの設定
| 項目             | 設定値                                                              |
|:---------------- |:------------------------------------------------------------------- |
| APP_PATH         | Google Chromeのファイル（chrome.exe）パス                           |
| DRIVER_PATH      | ChromeDriverのファイルパス                                          |
| LOG_PATH         | ログファイルパス（適当に）                                          |
| HOTEL_ID         | ホテル詳細ページのURLの「.../detail/XXXXX」の数値                   |
| ROOM_TYPE        | iniのコメントにある通り                                             |
| LOGIN_ADDRESS    | 東横インアカウントのメールアドレス                                  |
| LOGIN_PASS       | 東横インアカウントのパスワード                                      |
| LOGIN_TEL        | 電話番号                                                            |
| ENABLE_NOSMOKING | 禁煙ルームを検索する場合は 1                                        |
| ENABLE_SMOKING   | 喫煙ルームを検索する場合は 1                                        |
| PRIORITY         | 上記が両方1だった場合にどちらを先に検索するか（NOSMOKING, SMOKING） |
| CHKIN_VALUE      | チェックイン時刻                                                    |
| PRTSCR_PATH      | スクリーンショット保存パス                                          |

## CHKIN_VALUEに設定できる値
| 設定値   | ページ上の表記 |
|:--------:|:--------------:|
| 15:00:00 | 15:00～16:00   |
| 16:00:00 | 16:00～17:00   |
| 17:00:00 | 17:00～18:00   |
| 18:00:00 | 18:00～19:00   |
| 19:00:00 | 19:00～20:00   |
| 20:00:00 | 20:00～21:00   |
| 21:00:00 | 21:00～22:00   |
| 22:00:00 | 22:00～22:30   |
| 22:30:00 | 22:30～23:00   |
| 23:00:00 | 23:00～23:30   |
| 23:30:00 | 23:30～24:00   |

## つかいかた
スクリプトのフォルダでコマンドプロンプトを開き、以下のコマンドを実行します。  
※例：2018年1月1日を予約する場合
```
python Main.py 2018/01/01
```
中断する場合はコマンドプロンプトを閉じます。

## 注意事項
* **キャンセル規定**に十分注意してご利用下さい
* 公式HPの構成が変わることで使えなくなる可能性があります
* 連泊には対応していません
* 決済方法、領収書宛名などはアカウントに登録されているものとなります
* 実行間隔には十分な余裕を設定していますが、多重起動で実行し続けた場合、**不正アクセス**とみなされる可能性もありますので、ほどほどに使って下さい

## 更新履歴
| 日付       | 内容                                                 |
|:----------:|:---------------------------------------------------- |
| 2018/02/16 | ログフル時に落ちる問題など修正、エラー時スクショ保存 |
| 2018/02/10 | ログ修正、チェックイン日付をコマンドライン引数化     |
| 2018/02/06 | リリース                                             |
