#AlgoDesk 2025 Mallard-Dash
#main.py

import time
import datetime
import sqlite3
import login
import os
import pwinput
from users import User
from orders import Order_engine
import textual_dev as tx

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
        print(f"---Logged in as: {self.current_user} ---")

        
    def show_main_menu(self):
        while True:
            print("***Main menu***\n",
                "1. Check balance\n",
                "2. View transactions\n",
                "3. Order menu\n",
                "4. Active derivates\n",
                "5. Log off")
            menu_choice = input(f"Please enter a menu-choice: ")
            match menu_choice:
                case "1":
                    self.current_user.check_user_balance()
                case "2":
                    pass 
                case "3":
                    self.order.show_order_menu()
                case "4":
                    pass
                case "5":
                    break

    def fetch_API(self):
        pass


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