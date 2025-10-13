#AlgoDesk 2025 Mallard-Dash
#orders.py

import time
import datetime

class Order_engine():
    def __init__(self, user, kind, transaction_no): #long/short?
        self.user = user
        self.kind = kind
        self.transaction_no = transaction_no

    def __repr__(self):
        pass

    def show_order_menu():
        order_menu = True
        while order_menu:
            print("***Order-menu***\n",
                "1. Place new buy order\n",
                "2. Place new sell order\n",
                "3. Remove order\n",
                "4. Exit to main menu")
            menu_choice = input("Please choose a menu choice: ")
            match menu_choice:
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass

    def place_sell_order():
        pass

    def order_is_valid():
        pass

    def stop_loss_menu():
        pass

    def take_profit_menu():
        pass

    def courtage():
        pass

    def set_new_stop_loss():
        pass

    def remove_stop_loss():
        pass

    def move_stop_loss():
        pass

    def set_new_take_profit():
        pass

    def remove_take_profit():
        pass

    def move_take_profit():
        pass

    def triggered_stop_loss():
        pass

    def triggered_take_profit():
        pass

    def kind_of_ticker():
        pass