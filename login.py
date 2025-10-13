#AlgoDesk 2025 Mallard-Dash
#login.py

import time
import datetime
import sqlite3


def show_login_menu():
    login_menu = True
    while login_menu:
        print("***Login***\n",
              "1. Login existing user\n",
              "2. Create new user\n",
              "3. Exit program")
        menu_choice = input("Please choose a menu choice: ")
        match menu_choice:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass

def check_if_user_exists():
    pass