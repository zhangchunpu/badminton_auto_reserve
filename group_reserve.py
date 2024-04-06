import json
import time
from multiprocessing import Process

from reserve import reserve

"""
複数人で予約するときに使う関数．
"""
def group_reserve(event_id):
    with open("./users/users.json","r") as f: 
        users_info = json.load(f)
        print(f"{len(users_info)}人の予約をします．")
        for username, password in users_info.items():
            process = Process(target=reserve, args=(event_id,username,password))
            process.start()

"""
テスト書きたくないのでここでテスト
"""        
if __name__ == "__main__":
    group_reserve(100)