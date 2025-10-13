#AlgoDesk 2025 Mallard-Dash
#main.py

import time
import datetime
import sqlite3

class Main():
    def __init__(self):
        pass
        
    def show_main_menu(self):
        while True:
            print("***Main menu***\n",
                "1. Check balance\n",
                "2. View transactions\n",
                "3. Order menu\n",
                "4. Active derivates\n",
                "5. Log off")
            menu_choice = (f"Please enter a menu-choice: ")
            match menu_choice:
                case "1":
                    pass
                case "2":
                    pass 
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    pass

    def fetch_API(self):
        pass

    def create__user_database(self, db_name):
        db_name = input("Please enter a name for new database: ")
        conn = sqlite3.connect(f"{db_name}")
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE {db_name}(name, email, password, account_no)")

    def get_timestamp(self):
        time_data = datetime.datetime.now()
        time_h = time_data("%H")
        time_m = time_data("%M")
        date = date()
