import re
from bs4 import BeautifulSoup
from login import *

def replace_space(string):
    return re.sub(' +', ' ', string)

def print_reservation_info(elems):

    # ない場合はメッセージを出す
    if not elems:
        print("予約履歴はありません．WebPageから確認してください")
        return

    color_dic = {"black":"\033[30m", "red":"\033[31m", "green":"\033[32m", "yellow":"\033[33m", "blue":"\033[34m", "end":"\033[0m"}
    
    for elem in elems:
        #色をつけます
        place = elem.find("li",{"class":"b-name"}).text.strip()
        color_place = color_dic['blue']+replace_space(place)+color_dic['end']
        #色をつけます
        time = elem.find("li",{"class":"b-dayTime"}).text.strip()
        color_time = color_dic['blue']+replace_space(time)+color_dic['end']
        #色をつけます
        status = elem.find("li").text.strip()
        color_status = color_dic['red']+replace_space(status)+color_dic['end']
        #色をつけます
        reserve_id = elem.find("li",{"class":"b-confirm"}).find("a")["href"].split("/")[-1]
        color_reserve_id = color_dic['red']+replace_space(reserve_id)+color_dic['end']

        print(f"予約時間: {color_time}".ljust(45," ")+
              f"予約場所:　{color_place}".ljust(35, " ")+
              f"ステータス: {color_status}".ljust(30, " ")+
              f"予約ID: {color_reserve_id}".ljust(30, " "))
    return

def get_reservations_history():
    session = default_user_login()
    print("ページソースを取得...")
    history_page_source = session.get("https://koto-hsc3.revn.jp/reservations/history")
    soup = BeautifulSoup(history_page_source.text,features="html.parser")
    history_list = soup.find_all("ul", {"class": "list_body_line"})
    return history_list

def show_history():
    print_reservation_info(get_reservations_history())


