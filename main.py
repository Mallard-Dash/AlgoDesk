#AlgoDesk 2025 Mallard-Dash
#main.py (Reviderad för att inkludera Balance Menu)

import time
import datetime
import sqlite3
import login
import os
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    red = Fore.RED
    green = Fore.GREEN
    blue = Fore.BLUE
    mag = Fore.MAGENTA
    yel = Fore.YELLOW
    cyan = Fore.CYAN
    bold = Style.BRIGHT
    reset = Style.RESET_ALL
except ImportError:
    red = green = blue = mag = yel = cyan = bold = reset = ""

import pwinput 

from users import User
from orders import Order_engine
# import textual_dev as tx # Inte använd i denna fil

#Tell the program where to put the database-file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")
#Test line

class Main():
    def __init__(self, user_session_object, order_engine_object):
        self.current_user = user_session_object
        self.order = order_engine_object
        print(f"\n{green}--- Logged in as: {self.current_user.name} ---{reset}")

        
    def show_main_menu(self):
        while True:
            print(f"\n{mag}=" * 30)
            print(f"{mag}{bold}*** Main Menu ***{reset}")
            print(f"{mag}=" * 30)
            
            print(f"{cyan}1. {yel}Balance Management Menu{reset} (Deposit, Withdraw, Check Balance)") 
            print(f"{cyan}2. {green}Order Menu{reset} (Buy/Sell Stocks/Derivatives)")
            print(f"{cyan}3. {red}Log Off{reset}")
            print("-" * 30)

            menu_choice = input(f"{blue}{bold}➤ Please enter a menu-choice: {reset}").strip()
            
            match menu_choice:
                case "1":
                    self.current_user.show_balance_menu()
                case "2":
                    self.order.show_order_menu()
                case "3":
                    print(f"{yel}Logging off {self.current_user.name}... Goodbye!{reset}")
                    break
                case _:
                    print(f"{red}Invalid choice, please try again.{reset}")


    def get_timestamp(self):
        time_data = datetime.datetime.now()
        
        time_h = time_data.strftime("%H")
        time_m = time_data.strftime("%M")
        
        date = time_data.date()
        
        print(f"Date: {date}, Time: {time_h}:{time_m}")
        return time_data 

if __name__ == "__main__":
    
    while True:
        # 1. This returns a User object or False
        login_result = login.show_login_menu() 

        if login_result == False:
            break # User choose "Exit"
        
        if isinstance(login_result, User):
            
            order_app = Order_engine(current_user_object=login_result)
            
            main_app = Main(user_session_object=login_result, 
                            order_engine_object=order_app) 

            main_app.show_main_menu()