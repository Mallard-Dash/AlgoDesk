#AlgoDesk 2025 Mallard-Dash
#orders.py

import time
import datetime
import os
import yfinance as yf
from colorama import Fore, init
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW

class Order_engine():
    def __init__(self, user, kind, transaction_no): #long/short?
        self.user = user
        self.kind = kind
        self.transaction_no = transaction_no

    def buy_order_mem(self):
        buy_mem_dict = {"Ticker": self.ticker,
                        "Position": self.position,
                        "transaction_no": self.transaction_no,
                        "cost": self.cost,
                        "ammount": self.ammount}

    def show_order_menu(self):
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
                    self.buy_order()
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    break

    def buy_order(self):
        while True:
            print(f"{mag} |------------------------------------------------------------------------------|\n"
                f" |*************************Available tickers************************************|\n",
                f"{blue}|------------------------------------------------------------------------------|\n"
                f" {green}|Ticker|	{red}|Company /Asset|	        {yel}|Category              {blue}         |\n",
                f"{blue}|------------------------------------------------------------------------------|\n",
                f"{green}|1. AAPL   |  {red}|Apple Inc.                |{yel}|Big Tech Stock                      |\n",
                f"{green}|2. NVDA   |  {red}|Nvidia Corp.              |{yel}|AI/Semiconductor Stock              |\n",
                f"{green}|3. MSFT   |  {red}|Microsoft Corp.           |{yel}|Software Stock                      |\n",
                f"{green}|4. SPY    |  {red}|S&P 500   ETF Broad Market|{yel}|(Tracks the top 500 US companies)   |\n",
                f"{green}|5. GLD    |  {red}|SPDR Gold Shares          |{yel}|Commodity (Tracks the price of gold)|\n",
                f"{green}|6. USO    |  {red}|United States Oil Fund    |{yel}|Commodity (Tracks the price of oil) |\n",
                f"{green}|7. JPM    |  {red}|JPMorgan Chase & Co.      |{yel}|Finance/Bank Stock                  |\n",
                f"{green}|8. BTC-USD|  {red}|Bitcoin                   |{yel}|Cryptocurrency                      |\n",
                f"{blue}|------------------------------------------------------------------------------|")


            ticker = input("What ticker do you want to buy? Choose with the numbers listed to the left (To exit, press 9): ")
            match ticker:
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
                case "6":
                    pass
                case "7":
                    pass
                case "8":
                    pass
                case "9":
                    break



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
