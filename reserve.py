from bs4 import BeautifulSoup
import pandas as pd

from login import *
from get_badminton_info import get_badminton_events



def post_info(event_id,session):
    #予約する際に必要なuser_idを取得する
    home_source = session.get("https://koto-hsc3.revn.jp/").text
    user_id = BeautifulSoup(home_source, features="html.parser").find("li",{"title":"マイページ"}).find("a")["href"].split("/")[-1]
    
    #予約可能=枠が青のイベントからイベント番号と一致したイベントを探す
    events = [event for event in get_badminton_events() if event["data-event-id"] == str(event_id) and "rgb(107, 225, 255)" in event["style"]]
    
    if len(events) == 0:
        print("予約可能なイベントが見つかりませんでした")
        return
    
    # 予約可能なイベントでイベント番号が重複することはないので起こり得ないかなと
    elif len(events) > 1:
        print("イベントが2件見つかりました...")
        return
    
    event_url = events[0]["data-url"]
    
    #Query String Parametersを作成
    #確認ページから必要な認証情報を取得
    query_string_parameters = f"reservation_type=1&user_id={user_id}&event_id={event_id}&usage_timestamp_from={event_url.split('=')[-1]}"
    url = f"https://koto-hsc3.revn.jp/reservations/add?{query_string_parameters}"
    reserve_confirm_res = session.get(url)
    soup = BeautifulSoup(reserve_confirm_res.text,features="html.parser")

    try: 
        #予約するためのリクエストを作成する
        request_params = {}
        request_params["_csrfToken"] = soup.find("input",{"name": "_csrfToken"})["value"]
        request_params["_tokenValidation"] = soup.find("input",{"name": "_tokenValidation"})["value"]
        request_params["reservations[addition_values][item_25]"] = ""
        request_params["_Token[fields]"] = soup.find("input",{"name": "_Token[fields]"})["value"]
        request_params["_Token[unlocked]"] = ""
        #reserve
        cookies = reserve_confirm_res.cookies
        confirm_page_res = session.post(url, 
                                        data=request_params, 
                                        cookies=cookies)
        
        if confirm_page_res.status_code != 200:
            print("予約できませんでした．WebPageから操作してください")
            return
        
        #予約を確定するリクエストを取得
        soup = BeautifulSoup(confirm_page_res.text,features="html.parser")
        request_params = {}
        request_params["_csrfToken"] = soup.find("input",{"name": "_csrfToken"})["value"]
        request_params["_tokenValidation"] = soup.find("input",{"name": "_tokenValidation"})["value"]
        request_params["_Token[fields]"] = soup.find("input",{"name": "_Token[fields]"})["value"]
        request_params["_Token[unlocked]"] = ""
        cookies = confirm_page_res.cookies
        response = session.post("https://koto-hsc3.revn.jp/reservations/add-conf?key=0", 
                                        data=request_params, 
                                        cookies=cookies)
        if response.status_code != 200:
            print("予約できませんでした．WebPageから操作してください")
            return
        print("予約完了")

    except: 
        print("予約できませんでした．WebPageから操作してください")
    return

def reserve(event_id, user_id, password):
    session = login(user_id,password)
    if session is None:
        print(f"{user_id}のログインが失敗しました．")
        return
    print(f"{user_id}のログインが成功しました．") 
    return post_info(event_id,session)
    
def default_user_reserve(event_id):
    session = default_user_login()
    #予約する際に必要なuser_idを取得する
    return post_info(event_id,session)
    
        






   
    




