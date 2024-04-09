from bs4 import BeautifulSoup
from login import *

def cancel(reservation_id):
    session = default_user_login()

    try:
        reservation_page_source = session.get(f"https://koto-hsc3.revn.jp/reservations/view/{reservation_id}")
        cookies = reservation_page_source.cookies
        soup = BeautifulSoup(reservation_page_source.text,features="html.parser")
        csrf_token = soup.find("input",{"name": "_csrfToken"})["value"]
        token_fields = soup.find("input",{"name": "_Token[fields]"})["value"]
        token_unlocked = soup.find("input",{"name": "_Token[unlocked]"})["value"]
        #cancelするためのリクエストを作成する
        request_params = {}
        request_params["_csrfToken"] = csrf_token
        request_params["js_button_yes"] = "はい"
        request_params["js_button_no"] = "いいえ"
        request_params["_Token[fields]"] = token_fields
        request_params["_Token[unlocked]"] = token_unlocked
        #cancel
        response = session.post(f"https://koto-hsc3.revn.jp/reservations/cancel/{reservation_id}",data=request_params,cookies=cookies)
        if response.status_code == 200:
            print("完了")
        elif response.status_code == 400:
            print("キャンセル済みかも")
        else:
            print("WebPageから操作してください")
    except:
        print("予約IDが正しくない可能性があります")
    return
   
    




