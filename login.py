import requests
import getpass
import json

from bs4 import BeautifulSoup

# 必要最低限にしか書きたくないのでusername passwordは直で書いています．
username = "ユーザー名"
password = "パスワード"

login_url = "https://koto-hsc3.revn.jp/auth/login"
logout_url = "https://koto-hsc3.revn.jp/auth/logout"

def login(login_id,password):
    print("ログイン...")
    request_params = {}
    session = requests.session()
    response = session.get(login_url)

    soup = BeautifulSoup(response.text,features="html.parser")
    csrf_token = soup.find("input",{"name": "_csrfToken"})["value"]
    token_fields = soup.find("input",{"name": "_Token[fields]"})["value"]
    token_unlocked = soup.find("input",{"name": "_Token[unlocked]"})["value"]

    request_params["_csrfToken"] = csrf_token
    request_params["login_id"] = login_id
    request_params["password"] = password
    request_params["_Token[fields]"] = token_fields
    request_params["_Token[unlocked]"] = token_unlocked
    
    response_cookie = response.cookies
    
    response = session.post(login_url,data=request_params,cookies=response_cookie)
    # ここの例外ハンドリング変な感じなってますけど一旦無視
    try:
        if response.history[0].status_code == 302:
            return session
        else:
            return 
    except:
        return


"""
手動で
"""
def input_login():
    while True:
        username = None
        password = None
        username=getpass.getpass(prompt="ユーザー名:")
        password=getpass.getpass(prompt="パスワード:")
        session = login(username, password)
        if session is not None:
            print("ログイン成功")
            return session
        print("入力間違いがありました．再度入力してください")
        continue
    

def default_user_login():
    session = login(username, password)
    if session is not None:
        print("ログイン成功")
        return session
    print("パスワードとユーザー名を入力してください")
    session = input_login()
    return 

"""
Test
"""
if __name__ == "__main__":
    default_user_login()