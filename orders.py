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
        self.usd_to_sek_rate = self.get_usd_sek_rate()
        if self.usd_to_sek_rate:
            print(f"{green}--- USD/SEK rate loaded: {self.usd_to_sek_rate} ---")
        else:
            print(f"{red}--- WARNING: Could not load USD/SEK exchange rate. ---")

        print(f"{green}--- Order Engine Initialized for: {self.current_user.name} ---")

    def show_order_menu(self):
        """
        Main loop for the order menu.
        """
        while True:
            print(f"\n{mag}*** Order Menu ***")
            print("1. Place new buy order")
            print("2. Place new sell order")
            print("3. Remove order")
            print("4. Exit to main menu")
            
            menu_choice = input("Please choose an option: ")
            match menu_choice:
                case "1":
                    # This is the "controller" function that runs the whole buy process
                    self.execute_buy_trade()
                case "2":
                    print(f"{yel}Sell orders not implemented yet.")
                    pass
                case "3":
                    print(f"{yel}Removing orders not implemented yet.")
                    pass
                case "4.":
                    print("Returning to main menu...")
                    break
                case _:
                    print(f"{red}Invalid choice, please try again.")

    def get_usd_sek_rate(self):
        """
        Fetches the current USD to SEK exchange rate.
        """
        try:
            print("Fetching USD/SEK exchange rate...")
            # "SEK=X" is the yfinance ticker for USD/SEK
            rate_ticker = yf.Ticker("SEK=X")
            rate = rate_ticker.fast_info['lastPrice']
            return float(rate)
        except Exception as e:
            print(f"{red}Error fetching exchange rate: {e}")
            return None # Handle this error

    # -----------------------------------------------------------------
    # --- BUY ORDER PROCESS (Divided into steps) ---
    # -----------------------------------------------------------------

    def execute_buy_trade(self):
        """
        This is the main "controller" function for buying.
        It calls each step in order and cancels if any step fails.
        """
        # --- Step 1: Get Ticker ---
        ticker_symbol = self.select_ticker_from_menu()
        if not ticker_symbol:
            print("Returning to order menu...")
            time.sleep(1.5)
            return  # Exits the buy process

        # --- Step 2: Get Position Type ---
        position_type = self.get_position_type(ticker_symbol)
        if not position_type:
            print(f"{yel}Order cancelled.")
            return # Exits the buy process

        # --- Step 3: Get Price, Quantity, and Confirm ---
        # This one function handles price, quantity, balance, and confirmation
        trade_details = self.get_quantity_and_confirm(ticker_symbol, position_type)
        if not trade_details:
            print(f"{yel}Order cancelled.")
            return # Exits the buy process

        # --- Step 4: Commit to Database ---
        print(f"{green}Committing transaction...")
        try:
            self.commit_transaction_to_db(
                ticker=ticker_symbol,
                type=position_type,
                quantity=trade_details["quantity"],
                price_per_share=trade_details["price"]
            )
            # IMPORTANT: Update the user's balance after the trade
            new_balance = self.current_user.check_user_balance() - trade_details["total_cost"]
            self.current_user.update_user_balance(new_balance) 
            
            print(f"{green}Transaction successful! New balance: {new_balance:,.2f} SEK")
            time.sleep(2)
            
        except Exception as e:
            print(f"{red}FATAL ERROR: Could not commit transaction: {e}")

    def select_ticker_from_menu(self):
        """
        Step 1: Displays a dynamic menu from self.available_tickers.
        Returns the chosen ticker symbol (e.g., "AAPL") or None if user exits.
        """
        while True:
            print(f"\n{mag} |------------------------------------------------------------------------------|")
            print(f" |************************* Available Tickers ************************************|")
            print(f" {blue}|------------------------------------------------------------------------------|")
            print(f" {green}| # | Ticker  | Company / Asset               | Category                       |")
            print(f" {blue}|---|---------|-------------------------------|--------------------------------|")
            
            # --- This loop dynamically generates the menu ---
            for key, info in self.available_tickers.items():
                # Use ljust() to format columns neatly
                print(f" {green}| {key.ljust(1)} | {red}{info['symbol'].ljust(7)} {green}| {info['name'].ljust(29)} | {yel}{info['category'].ljust(30)} {green}|")
            print(f" {blue}|------------------------------------------------------------------------------|")
            
            choice = input("Choose a number to buy (or 9 to go back): ")
            
            selected_ticker = self.available_tickers.get(choice)
            
            if selected_ticker:
                if selected_ticker["symbol"] == "EXIT":
                    return None  # User chose to exit
                else:
                    return selected_ticker["symbol"]  # Returns "AAPL", "NVDA", etc.
            else:
                print(f"{red}Invalid choice '{choice}'. Please try again.")
                time.sleep(1)

    def get_position_type(self, ticker_symbol):
        """
        Step 2: Asks for 'long' or 'short' and returns the validated string.
        Returns 'long', 'short', or None if user cancels.
        """
        while True:
            # Use .strip() to remove whitespace and .upper() to simplify check
            kind = input(f"Would you like a {green}(long){yel} or {red}(short){yel} position in {ticker_symbol}? (Type 'c' to cancel): ").strip().upper()
            
            if kind == "LONG":
                return "long"
            elif kind == "SHORT":
                return "short"
            elif kind == "C":
                return None
            else:
                print(f"{red}Invalid input. Please choose 'long', 'short', or 'c'.")

    def get_current_price(self, ticker_symbol):
        """
        Helper: Fetches the current market price for a ticker.
        Returns the price as a float, or None if it fails.
        """
        print(f"Fetching current price for {ticker_symbol}...")
        try:
            ticker_obj = yf.Ticker(ticker_symbol)
            # .fast_info is much quicker than .info
            current_price = ticker_obj.fast_info['lastPrice']
            print(f"Current price for {ticker_symbol}: {current_price:,.2f} SEK")
            return float(current_price)
        except Exception as e:
            print(f"{red}Could not fetch price for {ticker_symbol}: {e}")
            return None

    def get_quantity_and_confirm(self, ticker_symbol, position_type):
        """
        Step 3: Gets quantity, fetches price, checks balance, and asks for final confirmation.
        """
        # First, check if your rate loaded correctly
        if not self.usd_to_sek_rate:
            print(f"{red}Cannot proceed: USD/SEK exchange rate is missing.")
            return None

        # --- First, get the price in USD ---
        price_per_share_usd = self.get_current_price(ticker_symbol) # This gets the USD price
        if price_per_share_usd is None:
            return None # Failed to get price

        # --- CONVERT THE PRICE ---
        price_per_share_sek = price_per_share_usd * self.usd_to_sek_rate

        while True:
            try:
                # 1. Get Quantity (no change here)
                quantity_str = input(f"How many shares of {ticker_symbol} would you like? (Type 'c' to cancel): ").strip()
                if quantity_str.lower() == 'c':
                    return None
                quantity = int(quantity_str)
                # ... (rest of quantity checks) ...

                # 2. Calculate Cost (NOW IN SEK)
                total_cost_sek = price_per_share_sek * quantity
                
                # 3. Check Balance (This comparison now makes sense!)
                balance = self.current_user.check_user_balance() 
                
                if total_cost_sek > balance:
                    print(f"{red}Insufficient funds!")
                    print(f"  Your balance: {balance:,.2f} SEK")
                    # Show the cost in both currencies for clarity
                    print(f"  Trade cost:   {total_cost_sek:,.2f} SEK")
                    print(f"  ({quantity} shares @ {price_per_share_sek:,.2f} SEK)")
                    print(f"{yel}Please enter a smaller quantity or 'c' to cancel.")
                    continue

                # 4. Show Confirmation Prompt (Updated to show SEK)
                print(f"\n{yel}--- PLEASE CONFIRM ---")
                print(f"  Ticker:    {ticker_symbol}")
                print(f"  Position:  {position_type.UPPER()}")
                print(f"  Quantity:  {quantity}")
                print(f"  Est. Price:{price_per_share_sek:,.2f} SEK  ({price_per_share_usd:,.2f} USD)")
                print(f"  {blue}------------------------")
                print(f"  Total Cost:{total_cost_sek:,.2f} SEK")
                print(f"  Remaining: {balance - total_cost_sek:,.2f} SEK")
                print(f"{yel}------------------------")

                choice = input(f"To confirm this transaction press 'Y'. To abort press 'N': ").strip().upper()

                if choice == "Y":
                    return {
                        "quantity": quantity, 
                        # IMPORTANT: Store the price in SEK in your database
                        "price": price_per_share_sek, 
                        "total_cost": total_cost_sek
                    }
                elif choice == "N":
                    return None # User aborted
                else:
                    print(f"{red}Invalid choice. Please press 'Y' or 'N'.")

            except ValueError:
                print(f"{red}Invalid input. Please enter a whole number for the quantity.")
            except Exception as e:
                print(f"{red}An error occurred: {e}")
                return None

    def commit_transaction_to_db(self, ticker, type, quantity, price_per_share):
        """
        Step 4: Executes the final SQL INSERT statement with all the collected data.
        """
        sql_query = """
        INSERT INTO Transactions (user_account_id, ticker, type, quantity, price_per_share, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        # Get the current time for the timestamp
        current_timestamp = datetime.datetime.now()
        
        data = (
                self.current_user.user_id, 
                ticker,
                type,
                quantity,
                price_per_share,
                current_timestamp
        )
        
        cur = self.con.cursor()
        cur.execute(sql_query, data)
        self.con.commit()


    def __del__(self):
        """
        A cleanup method to close the database connection
        when the Order_engine object is no longer needed.
        """
        print("Closing database connection...")
        self.con.close()
    
    def place_sell_order(self):
        pass

    def order_is_valid(self):
        pass