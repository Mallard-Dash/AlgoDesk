#AlgoDesk 2025 Mallard-Dash
#orders.py

import time
import datetime
import os
import yfinance as yf
from colorama import Fore, init
import textual_dev as tx
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW

AAPL_TICKER = yf.ticker("AAPL")
stock_info_AAPL = AAPL_TICKER.info
MSFT_TICKER = yf.ticker("MSFT")
stock_info_MSFT = MSFT_TICKER.info
SPY500_TICKER = yf.ticker("SPY S&P 500")
stock_info_SPY500 = SPY500_TICKER.info
GLD_TICKER = yf.ticker("GLD")
stock_info_GLD = GLD_TICKER.info
USO_TICKER = yf.ticker("USO")
stock_info_USO = USO_TICKER.info
JPM_TICKER = yf.ticker("JPM")
stock_info_JPM = JPM_TICKER.info
BTCUSD_TICKER = yf.ticker("BTC-USD")
stock_info_BTCUSD = BTCUSD_TICKER.info

class Order_engine():
    def __init__(self, user, kind, transaction_no): #long/short?
        self.user = user
        self.kind = kind
        self.transaction_no = transaction_no        


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


            self.ticker = input("What ticker do you want to buy? Choose with the numbers listed to the left (To exit, press 9): ")
            match ticker:
                case "1":
                    self.ticker = "AAPL"
                case "2":
                    self.ticker = "NVDA"
                case "3":
                    self.ticker = "MSFT"
                case "4":
                    self.ticker = "SPY"
                case "5":
                    self.ticker = "GLD"
                case "6":
                    self.ticker = "USO"
                case "7":
                    self.ticker = "JPM"
                case "8":
                    self.ticker = "BTC-USD"
                case "9":
                    print("Back to order-menu...")
                    time.sleep(1.5)
                    self.show_order_menu()

            sql_query = """
            INSERT INTO Transactions (user_account_id, ticker, type, quantity, price_per_share)
            VALUES (?, ?, ?, ?, ?)
            """
            data = (
                    self.user_account_id,
                    self.ticker,
                    self.type,
                    self.quantity,
                    self.price_per_share,
                    self.timestamp)

            cur = con.cursor()
            cur.execute(sql_query, data)
            con.commit()


    def buy_position(self):
        try:
            kind = str(input(f"Would you like a long or short position in {self.ticker}? (long/short)"))
        except ValueError:
            print("Wrong value-input!")
            continue
        if kind.upper() == "long":
            self.type = kind
            return
        elif kind.upper() == "short":
            self.type = kind
            return
        else:
            print("Please choose either a long or short position: ")

    def quantity(self):
        quantity = int(input(f"How many shares of {self.ticker} would you like to buy?"))


    def buy_cost(self):
        pass

    def buy_ammount(self):
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
        self.ticker = input("What ticker do you want to buy? Choose with the numbers listed to the left (To exit, press 9): ")
        match ticker:
                case "1":
                    self.ticker = "AAPL"
                case "2":
                    self.ticker = "NVDA"
                case "3":
                    self.ticker = "MSFT"
                case "4":
                    self.ticker = "SPY"
                case "5":
                    self.ticker = "GLD"
                case "6":
                    self.ticker = "USO"
                case "7":
                    self.ticker = "JPM"
                case "8":
                    self.ticker = "BTC-USD"
                case "9":
                    print("Back to order-menu...")
                    time.sleep(1.5)
                    self.show_order_menu()
