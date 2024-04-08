import time
import requests
import datetime
import unicodedata

from retry import retry
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://koto-hsc3.revn.jp/"

"""
見た目を整える用の関数
"""
def _align_text(text, length, fillchar=" "):
    count = sum(2 if unicodedata.east_asian_width(c) in 'FWA' else 1 for c in text)
    return fillchar*(length-count)+text

"""
イベントを画面に表示させる関数
"""
def _print_day_place_info(elems):
    line_to_print = []
    weekdays = {0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日"}
    
    for elem in elems:
        date_str = elem["data-usage-timestamp"]
        dt = datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M')
        d = dt.day
        event_id = elem["data-event-id"]
        background_color = elem["style"]
        # 枠の色でクリックできるか=予約できるかを判定
        if "rgb(107, 225, 255)" in background_color:
                line_to_print.append((f"{d}日".rjust(4," "), 
                                      _align_text(elem.text.strip(),25), 
                                      weekdays[dt.weekday()].rjust(5, " "), 
                                      event_id.rjust(5, " "),
                                      "<- 予約可能"))
        else:
            line_to_print.append((f"{d}日".rjust(4," "), 
                                _align_text(elem.text.strip(),25), 
                                weekdays[dt.weekday()].rjust(5, " "), 
                                event_id.rjust(5, " ")))
    
    for line in line_to_print:
        print(" ".join(line))

def show_badminton_days():
    _print_day_place_info(get_badminton_events())

@retry(exceptions=Exception, tries=4, delay=2)
def get_badminton_events():
    
    session = requests.session()
    response = session.get(url)

    #ホームページのソースをBeautifulを用いて解析
    soup = BeautifulSoup(response.text,features="html.parser")

    #体育館と競技を選択した際のリクエストを作成
    csrf_token = soup.find("input",{"name": "_csrfToken"})["value"]
    token_fields = soup.find("input",{"name": "_Token[fields]"})["value"]
    token_unlocked = soup.find("input",{"name": "_Token[unlocked]"})["value"]
    request_params = {}
    request_params["_csrfToken"] = csrf_token
    request_params["_Token[fields]"] = token_fields
    request_params["_Token[unlocked]"] = token_unlocked
    request_params["select_parent_id[1]"] = ""
    request_params["label_id"] = ""
    request_params["label_select_type"] = "other"
    request_params["null"] = ""
    request_params["tag_id"] = ""
    request_params["tag_id[5][24]"] = "24" # 施設：江東区スポーツ会館
    request_params["tag_id[5][29]"] = "29" # 施設：深川北スポーツセンター
    request_params["tag_id[3][10]"] = "10" # 種目：バドミントン
    res = session.post(url,request_params)
    
    #カレンダのページソースを取得
    print("イベント取得中...")
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(res.url)
    
    #時間を置いてページソースを取得する
    time.sleep(1) # カレンダー表示まで少し時間があるのでsleep
    html = driver.page_source
    soup = BeautifulSoup(html,features="html.parser")

    #枠がある日を取得
    #子要素があればその日に枠がある
    events = soup.find("table",{"class": "timeTable month_table"}).select("tbody tr td div")
    return events


"""
テスト書きたくないのでここでテスト
"""
if __name__ == "__main__":
    show_badminton_days()