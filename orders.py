#AlgoDesk 2025 Mallard-Dash
#orders.py

import time
import datetime
import os
import yfinance as yf
from colorama import Fore, init
# import textual_dev as tx # Not used in this file
from users import User
import sqlite3 # You need to import this to use 'con'

# --- Color setup ---
init(autoreset=True) 
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW

# --- Database setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")

class Order_engine():
    """
    Manages placing, tracking, and executing buy/sell orders.
    """
    def __init__(self, current_user_object: User):
        self.current_user = current_user_object
        self.con = sqlite3.connect(DB_PATH) # Create and store the DB connection

        self.setup_database()
        
        self.available_tickers = {
            "1": {"symbol": "AAPL", "name": "Apple Inc.", "category": "Big Tech Stock"},
            "2": {"symbol": "NVDA", "name": "Nvidia Corp.", "category": "AI/Semiconductor Stock"},
            "3": {"symbol": "MSFT", "name": "Microsoft Corp.", "category": "Software Stock"},
            "4": {"symbol": "SPY", "name": "S&P 500 ETF", "category": "Broad Market ETF"},
            "5": {"symbol": "GLD", "name": "SPDR Gold Shares", "category": "Commodity (Gold)"},
            "6": {"symbol": "USO", "name": "United States Oil Fund", "category": "Commodity (Oil)"},
            "7.": {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "category": "Finance/Bank Stock"},
            "8": {"symbol": "BTC-USD", "name": "Bitcoin", "category": "Cryptocurrency"},
            "9": {"symbol": "EXIT", "name": "Back to order menu", "category": ""}
        }

    def setup_database(self):
        """
        Sets up the orders database table if it doesn't exist.
        """
        cursor = self.con.cursor()
        try:
            cursur = self.con.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    symbol TEXT,
                    order_type TEXT,
                    quantity INTEGER,
                    price REAL,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.con.commit()
            print("Transaction table status: Ready.")
        except sqlite3.Error as e:
            print(f"{red}Databasfel vid setup_database: {e}")

    def show_order_menu(self):
        """
        Main loop for the order menu.
        """
        while True:
            print(f"\n{mag}*** Order Menu ***")
            print("1. Place new buy order")
            print("2. Place new sell order")
            print("3. Exit to main menu")
            
            menu_choice = input("Please choose an option: ")
            match menu_choice:
                case "1":
                    # This is the "controller" function that runs the whole buy process
                    self.place_buy_order()
                case "2":
                    self.place_sell_order()
                case "3":
                    print("Returning to main menu...")
                    break
                case _:
                    print(f"{red}Invalid choice, please try again.")

    def get_ticker_prices(self, symbol: str):
        """
        Fetches the current price for a given ticker symbol using yfinance.
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                current_price = data['Close'][0]
                return current_price
            else:
                print(f"{red}No data found for symbol: {symbol}")
                return None
        except Exception as e:
            print(f"{red}Error fetching price for {symbol}: {e}")
            return None
        
    def execute_buy_order(self, symbol: str, quantity: int, price: float):
        """
        Executes a buy order and records it in the database.
        """
        cursor = self.con.cursor()
        try:
            cursor.execute('''
                INSERT INTO orders (user_id, symbol, order_type, quantity, price, status)
                VALUES (?, ?, 'BUY', ?, ?, 'EXECUTED')
            ''', (self.current_user.id, symbol, quantity, price))
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(f"{red}Database error while executing buy order: {e}")
            return False

    def place_buy_order(self):
        for i in self.available_tickers:
            ticker = self.available_tickers[i]
            print(Fore.CYAN + f"{i}. {ticker['name']} ({ticker['symbol']}) - {ticker['category']}\n")
        ticker_choice = input("Choose which ticker you want to buy (# 1-9): ").strip()
        if str(ticker_choice) == "9" or ticker_choice.upper() == "EXIT":
            print("Returning to order menu...")
            return
        ticker_info = self.available_tickers.get(str(ticker_choice))
        if not ticker_info:
            print(f"{red}Invalid ticker choice.")
            return
        price = self.get_ticker_prices(symbol=ticker_info['symbol'])
        if price is None:
            print(f"{red}Could not retrieve price for {ticker_info['symbol']}.")
            return

        try:
            quantity = int(input(f"How many shares of {ticker_info['symbol']} do you want to buy? "))
            if quantity <= 0:
                print(f"{red}Quantity must be a positive integer.")
                return
        except ValueError:
            print(f"{red}Invalid quantity input.")
            return
        total_cost = quantity * price
        user_capital = self.current_user.capital
        if total_cost > user_capital:
            print(f"{red}Insufficient funds. You need ${total_cost:.2f} but have ${user_capital:.2f}.")
            return
        # Place the order in the database
        print(f"Order summary: Buy {quantity} shares of {ticker_info['symbol']} at ${price:.2f} each for a total of ${total_cost:.2f}.")
        confirm = input("Confirm order? (y/n): ")
        if confirm.lower() == 'y':
            try:
                success = self.execute_buy_order(ticker_info['symbol'], quantity, price)
                if success:
                    print(f"{green}Order placed successfully!")
                    # Deduct the amount from user's capital
                    self.current_user.capital -= total_cost
                    # Persist the updated balance to the DB
                    try:
                        self.current_user.save(self.con)
                    except Exception as e:
                        print(f"{red}Warning: failed to persist user balance: {e}")
                else:
                    print(f"{red}Failed to place order.")
            except sqlite3.Error as e:
                print(f"{red}Database error while placing order: {e}")
        else:
            print("Order cancelled.")

    def execute_sell_order(self, symbol: str, quantity: int, price: float):

        cursor = self.con.cursor()
        try:
            cursor.execute('''
                INSERT INTO orders (user_id, symbol, order_type, quantity, price, status)
                VALUES (?, ?, 'SELL', ?, ?, 'EXECUTED')
            ''', (self.current_user.id, symbol, quantity, price))
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(f"{red}Database error while executing sell order: {e}")
            return False

    def place_sell_order(self):
        portfolio = self.get_user_portfolio()
        
        if not portfolio:
            print(f"{yel}No assets to sell.")
            time.sleep(2)
            return

        print(f"\n{mag}*** Your assets ***")
        sellable_assets = list(portfolio.keys())
        for i, symbol in enumerate(sellable_assets):
            print(f"{i+1}. {symbol} (You own {portfolio[symbol]} shares)")
        print(f"{i+2}. EXIT - Return to order menu")

        try:
            choice_index = int(input("Which asset do you want to sell? (#): ")) - 1

            if choice_index == len(sellable_assets):
                print("Returning to order menu...")
                return
                
            symbol_to_sell = sellable_assets[choice_index]
            shares_owned = portfolio[symbol_to_sell]

        except (ValueError, IndexError):
            print(f"{red}Invalid selection.")
            return

        try:
            quantity_to_sell = int(input(f"How many of your {shares_owned} shares of {symbol_to_sell} do you want to sell? "))

            if quantity_to_sell <= 0:
                print(f"{red}Quantity must be a positive number.")
                return
            if quantity_to_sell > shares_owned:
                print(f"{red}You cannot sell more than you own (you have {shares_owned} shares).")
                return
        except ValueError:
            print(f"{red}Invalid quantity.")
            return

        price = self.get_ticker_prices(symbol=symbol_to_sell)
        if price is None:
            print(f"{red}Could not retrieve price for {symbol_to_sell}. Aborting.")
            return
            
        total_proceeds = quantity_to_sell * price

        print(f"Order: Sell {quantity_to_sell} shares of {symbol_to_sell} at ${price:.2f} each.")
        print(f"Total proceeds: ${total_proceeds:.2f}")
        confirm = input("Confirm sell order? (y/n): ")

        if confirm.lower() == 'y':
            success = self.execute_sell_order(symbol_to_sell, quantity_to_sell, price)
            
            if success:
                print(f"{green}Sell order placed!")
                # Add the proceeds to the user's capital
                self.current_user.capital += total_proceeds

                try:
                    self.current_user.save(self.con)
                    print(f"New balance: ${self.current_user.capital:.2f}")
                except Exception as e:
                    print(f"{red}Warning: failed to save user's balance: {e}")
            else:
                print(f"{red}Failed to place sell order.")
        else:
            print("SSell order cancelled.")

    def get_user_portfolio(self):
        portfolio = {}
        cursor = self.con.cursor()
        try:
            cursor.execute('''
                SELECT symbol, order_type, quantity 
                FROM orders 
                WHERE user_id = ? AND status = 'EXECUTED' 
            ''', (self.current_user.id,)) 
            
            all_orders = cursor.fetchall()
            
            for order in all_orders:
                symbol, order_type, quantity = order
                
                if symbol not in portfolio:
                    portfolio[symbol] = 0
                
                if order_type == 'BUY':
                    portfolio[symbol] += quantity
                elif order_type == 'SELL':
                    portfolio[symbol] -= quantity
            
            final_portfolio = {symbol: qty for symbol, qty in portfolio.items() if qty > 0}
            return final_portfolio
            
        except sqlite3.Error as e:
            print(f"{red}Database error while fetching portfolio: {e}")
            return {}

