#!/Users/chunpu/.pyenv/shims/python

import argparse
import sys
import os

from cancel import cancel
from login import login 
from get_badminton_info import *
from get_reservation_history import *
from reserve import *
from group_reserve import group_reserve

sys.stderr = open(os.devnull, "w")

def main(args):
    if args.action == "reserve":
        default_user_reserve(int(args.id))
    elif args.action == "cancel":
        cancel(int(args.id))
    elif args.action == "show":
        show_badminton_days()
    elif args.action == "group-reserve":
        group_reserve(int(args.id))
    else:
        show_history()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="main.py", add_help=True)

    #第一引数
    parser.add_argument("action", choices=["reserve", "show", "cancel", "history", "group-reserve"], default="show")
    
    #第二引数
    parser.add_argument("id", nargs="?", default=argparse.SUPPRESS)

    args = parser.parse_args()
    
    if args.action in ["reserve", "cancel", "group-reserve"] and not "id" in args:
        parser.error(f"予約やキャンセルの際にイベントidもしくは予約idを指定してください")

    if args.action == "show" and "id" in args:
        parser.error(f"引数エラー:showには引数は不要")
    
    main(args)
   
    
