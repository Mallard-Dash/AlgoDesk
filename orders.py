# orders.py (Revised with Long/Short functionality for derivatives)

import time
import datetime
import os
import yfinance as yf
from colorama import Fore, init, Style
from users import User
import sqlite3

# --- Color setup ---
init(autoreset=True) 
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW
cyan = Fore.CYAN
reset = Style.RESET_ALL
bold = Style.BRIGHT 

# Derivative symbol to handle as Long/Short
DERIVATIVE_SYMBOL = "BTC-USD"

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
        self.con = sqlite3.connect(DB_PATH)

        self.setup_database()
        
        self.available_tickers = {
            "1": {"symbol": "AAPL", "name": "Apple Inc.", "category": "Big Tech Stock"},
            "2": {"symbol": "NVDA", "name": "Nvidia Corp.", "category": "AI/Semiconductor Stock"},
            "3": {"symbol": "MSFT", "name": "Microsoft Corp.", "category": "Software Stock"},
            "4": {"symbol": "SPY", "name": "S&P 500 ETF", "category": "Broad Market ETF"},
            "5": {"symbol": "GLD", "name": "SPDR Gold Shares", "category": "Commodity (Gold)"},
            "6": {"symbol": "USO", "name": "United States Oil Fund", "category": "Commodity (Oil)"},
            "7": {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "category": "Finance/Bank Stock"},
            "8": {"symbol": DERIVATIVE_SYMBOL, "name": "Bitcoin (Derivat)", "category": "Cryptocurrency"}, # Changed description
            "9": {"symbol": "EXIT", "name": "Back to order menu", "category": ""}
        }

    def setup_database(self):
        """
        Sets up the orders database table if it doesn't exist.
        Adds position_type column.
        """
        cursor = self.con.cursor()
        try:
            # Updated table structure with position_type
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    symbol TEXT,
                    order_type TEXT,        -- BUY / SELL / LONG / SHORT
                    position_type TEXT,     -- LONG / SHORT / NULL
                    quantity INTEGER,
                    price REAL,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Add position_type to existing tables if missing
            try:
                cursor.execute("SELECT position_type FROM orders LIMIT 1")
            except sqlite3.OperationalError:
                cursor.execute("ALTER TABLE orders ADD COLUMN position_type TEXT")
                
            self.con.commit()
            print(f"\n{green}{bold}🚀 Database Status:{reset} {green}Orders table is ready (Position support enabled).")
        except sqlite3.Error as e:
            print(f"\n{red}{bold}❌ Database Error:{reset} {red}Failed to set up orders table: {e}")

    def show_order_menu(self):
        """
        Main loop for the order menu.
        """
        while True:
            print(f"\n{mag}=" * 40)
            print(f"{mag}{bold}*** AlgoDesk Trading Menu (User: {self.current_user.name}) ***")
            print(f"{mag}=" * 40)
            print(f"{cyan}1. {reset}Place new {green}BUY{reset} order (Stocks/ETFs)")
            print(f"{cyan}2. {reset}Place new {red}SELL{reset} order (Stocks/ETFs)")
            # --- NEW MENU OPTION FOR DERIVATIVES ---
            print(f"{cyan}3. {reset}Close {yel}Derivative Position (BTC){reset}") 
            # 4 is now transaction history
            print(f"{cyan}4. {reset}View {yel}Transaction History{reset}") 
            # 5 is now Exit
            print(f"{cyan}5. {reset}Exit to main menu")
            print("-" * 40)
            
            menu_choice = input(f"{blue}{bold}➤ Please choose an option (1-5): {reset}").strip()
            match menu_choice:
                case "1":
                    self.place_buy_order()
                case "2":
                    self.place_sell_order()
                case "3":
                    # --- NEW FUNCTION ---
                    self.close_derivative_position()
                case "4":
                    self.show_transaction_history()
                case "5":
                    print(f"{yel}Returning to main menu...{reset}")
                    break
                case _:
                    print(f"{red}Invalid choice: '{menu_choice}'. Please try again.")

    def get_ticker_prices(self, symbol: str):
        # ... (No changes) ...
        try:
            ticker = yf.Ticker(symbol)
            # For derivatives like BTC-USD we sometimes need another fetch if 1m interval fails
            data = ticker.history(period="1d", interval="1m") 
            if data.empty:
                data = ticker.history(period="1d") # Fallback
            
            if not data.empty:
                # Use the latest price if available
                current_price = data['Close'][-1] 
                return current_price
            else:
                return None
        except Exception as e:
            # print(f"Debug: Error fetching price for {symbol}: {e}")
            return None
        
    def execute_order(self, symbol: str, quantity: int, price: float, order_type: str, position_type: str = None):
        """
        Generic function to execute and save all types of orders.
        """
        cursor = self.con.cursor()
        try:
            cursor.execute('''
                INSERT INTO orders (user_id, symbol, order_type, position_type, quantity, price, status)
                VALUES (?, ?, ?, ?, ?, ?, 'EXECUTED')
            ''', (self.current_user.id, symbol, order_type, position_type, quantity, price))
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(f"{red}Database error while executing order: {e}")
            return False

    def place_buy_order(self):
        print(f"\n{green}{bold}*** Place Buy Order / Open Derivative Position ***{reset}")
        print(f"{yel}Available Capital: ${self.current_user.capital:,.2f}{reset}\n")
        
        # Print available tickers (no change here)
        print(f"{bold}{blue}# | Symbol | Name (Category){reset}")
        print("-" * 40)
        for i in self.available_tickers:
            ticker = self.available_tickers[i]
            if ticker['symbol'] == "EXIT":
                print(f"{mag}{i}. {bold}{ticker['symbol']:<6}{reset}{mag}| {ticker['name']}{reset}")
            else:
                # Mark the derivative symbol
                sym_color = yel if ticker['symbol'] == DERIVATIVE_SYMBOL else cyan
                print(f"{i}. {sym_color}{ticker['symbol']:<6}{reset}| {ticker['name']} ({ticker['category']})")

        ticker_choice = input(f"\n{blue}Choose which ticker to buy (1-9): {reset}").strip()
        
        if ticker_choice == "9" or ticker_choice.upper() == "EXIT":
            print(f"{yel}Returning to order menu...{reset}")
            return
            
        ticker_info = self.available_tickers.get(ticker_choice)
        if not ticker_info:
            print(f"{red}Invalid ticker choice: {ticker_choice}.{reset}")
            return
            
        symbol = ticker_info['symbol']
        
        # --- NEW DERIVATIVE LOGIC ---
        position_type = None
        order_type_str = "BUY"
        if symbol == DERIVATIVE_SYMBOL:
            print(f"\n{bold}{yel}DERIVATIVE SELECTED: {symbol}{reset}")
            deriv_choice = input(f"{blue}Do you want to go (L)ong or (S)hort? {reset}").strip().upper()
            if deriv_choice == 'L':
                position_type = 'LONG'
                order_type_str = 'LONG' # Use 'LONG' as order_type
                print(f"{green}Opening a {bold}LONG{reset}{green} position.{reset}")
            elif deriv_choice == 'S':
                position_type = 'SHORT'
                order_type_str = 'SHORT' # Use 'SHORT' as order_type
                print(f"{red}Opening a {bold}SHORT{reset}{red} position.{reset}")
            else:
                print(f"{red}Invalid choice for position type. Aborting.{reset}")
                return
        # --- END DERIVATIVE LOGIC ---
            
        # Fetch price
        print(f"{cyan}Fetching current price for {symbol}...{reset}")
        price = self.get_ticker_prices(symbol=symbol)
        if price is None:
            print(f"{red}Could not retrieve price for {symbol}. Aborting.{reset}")
            return

        print(f"{green}{symbol} Current Price: ${price:,.2f}{reset}")

        try:
            quantity = int(input(f"{blue}How many shares/units of {symbol} do you want to buy? {reset}"))
            if quantity <= 0:
                print(f"{red}Quantity must be a positive integer (greater than 0).{reset}")
                return
        except ValueError:
            print(f"{red}Invalid quantity input. Must be a number.{reset}")
            return
            
        total_cost = quantity * price
        user_capital = self.current_user.capital
        
        if total_cost > user_capital:
            print("-" * 50)
            print(f"{red}{bold}❌ INSUFFICIENT FUNDS!{reset}")
            print(f"{red}You need: ${total_cost:,.2f}{reset}")
            print(f"{red}You have: ${user_capital:,.2f}{reset}")
            print("-" * 50)
            return
            
        # Order summary
        print(f"\n{mag}*** Order Summary ***{reset}")
        print(f"{mag}Ticker:{reset} {symbol}")
        print(f"{mag}Type:{reset} {order_type_str}")
        print(f"{mag}Quantity:{reset} {quantity}")
        print(f"{mag}Price/unit:{reset} ${price:,.2f}")
        print(f"{mag}Total Cost:{reset} {bold}${total_cost:,.2f}{reset}")
        print("-" * 25)
        
        confirm = input(f"{blue}Confirm order? (y/n): {reset}").strip().lower()
        if confirm == 'y':
            try:
                # Use the generic execute_order
                success = self.execute_order(symbol, quantity, price, order_type_str, position_type)
                if success:
                    print(f"\n{green}{bold}✅ ORDER EXECUTED!{reset}")
                    print(f"{green}Opened {order_type_str} position for {quantity} units of {symbol} for ${total_cost:,.2f}.{reset}")
                    
                    self.current_user.capital -= total_cost
                    try:
                        self.current_user.save(self.con)
                        print(f"{green}New Balance: ${self.current_user.capital:,.2f}{reset}")
                    except Exception as e:
                        print(f"{red}Warning: failed to persist user balance: {e}")
                else:
                    print(f"{red}Failed to place order due to a database issue.{reset}")
            except sqlite3.Error as e:
                print(f"{red}Database error while placing order: {e}")
        else:
            print(f"{yel}Order cancelled.{reset}")

    # This function is for SELLING traditional assets (stocks/ETFs)
    def place_sell_order(self):
        # ... (Logic for selling traditional assets should remain the same) ...
        
        portfolio = self.get_user_portfolio()
        
        # Filter out derivative positions (Long/Short) from the traditional sell menu
        filtered_portfolio = {k: v for k, v in portfolio.items() if k != DERIVATIVE_SYMBOL or v[1] is None}
        
        if not filtered_portfolio:
            print(f"\n{yel}No traditional assets to sell. Use 'Close Derivative Position' for BTC.{reset}")
            time.sleep(3)
            return

        print(f"\n{red}{bold}*** Place Traditional Sell Order ***{reset}")
        print(f"\n{mag}*** Your Stock/ETF Assets ***{reset}")
        print(f"{blue}{bold}# | Symbol | Shares Owned{reset}")
        print("-" * 30)
        
        sellable_assets = list(filtered_portfolio.keys())
        for i, symbol in enumerate(sellable_assets):
            # Portfolio object now has (quantity, position_type)
            shares_owned = filtered_portfolio[symbol][0] 
            print(f"{i+1}. {cyan}{symbol:<6}{reset}| {shares_owned:<12}")
        
        exit_option_index = len(sellable_assets) + 1
        print(f"{mag}{exit_option_index}. {bold}EXIT{reset}{mag} - Return to order menu{reset}")
        print("-" * 30)

        # Rest of logic to choose asset, quantity and execute the sale...
        try:
            choice_input = input(f"{blue}Which asset do you want to sell? ({1}-{exit_option_index}): {reset}").strip()
            choice_index = int(choice_input) - 1

            if choice_index == len(sellable_assets):
                print(f"{yel}Returning to order menu...{reset}")
                return
            
            symbol_to_sell = sellable_assets[choice_index]
            shares_owned = filtered_portfolio[symbol_to_sell][0] # Get quantity

        except (ValueError, IndexError):
            print(f"{red}Invalid selection: '{choice_input}'.{reset}")
            return

        try:
            quantity_to_sell = int(input(f"{blue}How many of your {shares_owned} shares of {symbol_to_sell} do you want to sell? {reset}"))

            if quantity_to_sell <= 0:
                print(f"{red}Quantity must be a positive number (greater than 0).{reset}")
                return
            if quantity_to_sell > shares_owned:
                print(f"{red}You cannot sell more than you own (You own {shares_owned} shares).{reset}")
                return
        except ValueError:
            print(f"{red}Invalid quantity. Must be a whole number.{reset}")
            return

        print(f"{cyan}Fetching current price for {symbol_to_sell} for sale calculation...{reset}")
        price = self.get_ticker_prices(symbol=symbol_to_sell)
        if price is None:
            print(f"{red}Could not retrieve price for {symbol_to_sell}. Aborting.{reset}")
            return
            
        total_proceeds = quantity_to_sell * price

        print(f"\n{mag}*** Sell Order Summary ***{reset}")
        print(f"{mag}Ticker:{reset} {symbol_to_sell}")
        print(f"{mag}Quantity:{reset} {quantity_to_sell}")
        print(f"{mag}Sale Price/share:{reset} ${price:,.2f}")
        print(f"{mag}Total Proceeds:{reset} {bold}${total_proceeds:,.2f}{reset}")
        print("-" * 30)
        
        confirm = input(f"{blue}Confirm sell order? (y/n): {reset}").strip().lower()

        if confirm == 'y':
            # Use the generic execute_order with order_type='SELL' and position_type=None
            success = self.execute_order(symbol_to_sell, quantity_to_sell, price, 'SELL', None)
            
            if success:
                print(f"\n{green}{bold}✅ SELL ORDER EXECUTED!{reset}")
                print(f"{green}Sold {quantity_to_sell} shares of {symbol_to_sell} for ${total_proceeds:,.2f}.{reset}")
                
                self.current_user.capital += total_proceeds

                try:
                    self.current_user.save(self.con)
                    print(f"{green}Proceeds added to capital.{reset}")
                    print(f"{green}New Capital Balance: ${self.current_user.capital:,.2f}{reset}")
                except Exception as e:
                    print(f"{red}Warning: failed to save user's balance: {e}")
            else:
                print(f"{red}Failed to place sell order due to a database issue.{reset}")
        else:
            print(f"{yel}Sell order cancelled.{reset}")
            
    # --- NEW FUNCTION: CLOSE DERIVATIVE ---
    def close_derivative_position(self):
        """
        Shows open derivative positions, calculates P&L when closing,
        and updates the user's capital.
        """
        print(f"\n{yel}{bold}*** Close Derivative Position ({DERIVATIVE_SYMBOL}) ***{reset}")
        
        cursor = self.con.cursor()
        try:
            # Fetch all OPEN positions (Long/Short order_type) for BTC-USD
            # In a real simulation engine you'd group positions here
            # but for simplicity we fetch all opening orders.
            cursor.execute('''
                SELECT order_id, symbol, order_type, position_type, quantity, price, timestamp
                FROM orders
                WHERE user_id = ? 
                AND symbol = ? 
                AND order_type IN ('LONG', 'SHORT')
            ''', (self.current_user.id, DERIVATIVE_SYMBOL))
            
            open_positions = cursor.fetchall()

            if not open_positions:
                print(f"{mag}No open derivative positions to close.{reset}")
                time.sleep(2)
                return

            # Show open positions
            print(f"\n{mag}*** Open Positions ***{reset}")
            header_len = 70
            print("-" * header_len)
            print(f"{bold}{cyan}{'#':<4} | {'TYPE':<6} | {'QTY':<6} | {'ENTRY PRICE':>15} | {'TIMESTAMP':<20}{reset}")
            print("-" * header_len)

            position_map = {}
            for i, pos in enumerate(open_positions):
                order_id, symbol, order_type, position_type, quantity, price, timestamp = pos
                position_map[i + 1] = pos # Map menu choice to database row
                
                color = green if position_type == 'LONG' else red
                
                row = (
                    f"{i+1:<4} | "
                    f"{color}{position_type:<6}{reset} | "
                    f"{quantity:<6} | "
                    f"${price:>14,.2f} | "
                    f"{timestamp:<20}"
                )
                print(row)
            
            print("-" * header_len)
            
            # Choose position to close
            choice = input(f"{blue}Enter the # of the position to close: {reset}").strip()
            try:
                choice_index = int(choice)
                if choice_index not in position_map:
                    print(f"{red}Invalid selection.{reset}")
                    return
            except ValueError:
                print(f"{red}Invalid input. Must be a number.{reset}")
                return

            chosen_position = position_map[choice_index]
            order_id, symbol, _, position_type, quantity, entry_price, _ = chosen_position

            print(f"{cyan}Fetching current market price for {symbol} to calculate P&L...{reset}")
            current_price = self.get_ticker_prices(symbol=symbol)
            if current_price is None:
                print(f"{red}Could not retrieve current price. Aborting.{reset}")
                return
            
            # Calculate profit/loss (P&L)
            price_change = current_price - entry_price
            
            if position_type == 'LONG':
                pnl = price_change * quantity
                closing_order_type = 'SELL'
            elif position_type == 'SHORT':
                # If short, you profit when price goes DOWN (negative price_change)
                pnl = -(price_change * quantity)
                closing_order_type = 'BUY' # Short position is closed by buying back

            total_return = (quantity * entry_price) + pnl
            
            pnl_color = green if pnl >= 0 else red
            
            # Print calculation
            print(f"\n{mag}*** Closing Calculation ***{reset}")
            print(f"{mag}Position Type:{reset} {position_type}")
            print(f"{mag}Entry Price:{reset} ${entry_price:,.2f}")
            print(f"{mag}Closing Price:{reset} ${current_price:,.2f}")
            print(f"{mag}Quantity:{reset} {quantity}")
            print("-" * 30)
            print(f"{pnl_color}{bold}P&L (Profit/Loss): ${pnl:,.2f}{reset}")
            print(f"{mag}Original Cost (Capital Return): ${quantity * entry_price:,.2f}{reset}")
            print(f"{bold}Total Funds Added:{reset} ${total_return:,.2f}")
            print("-" * 30)

            confirm = input(f"{blue}Confirm closing this position? (y/n): {reset}").strip().lower()
            if confirm == 'y':
                # 1. Record closing order (SELL/BUY to close)
                # Use current_price * quantity as the amount for the closing order in transaction history.
                success = self.execute_order(symbol, quantity, current_price, closing_order_type, position_type="CLOSED")

                if success:
                    # 2. Update user's capital (Return stake + PnL)
                    self.current_user.capital += total_return
                    self.current_user.save(self.con)
                    
                    # 3. Mark the original LONG/SHORT order as closed so it doesn't show again
                    cursor.execute('''
                        UPDATE orders 
                        SET status = 'CLOSED', position_type = 'CLOSED' 
                        WHERE order_id = ?
                    ''', (order_id,))
                    self.con.commit()
                    
                    print(f"\n{green}{bold}✅ POSITION CLOSED!{reset}")
                    print(f"{pnl_color}P&L of ${pnl:,.2f} recorded.{reset}")
                    print(f"{green}New Capital Balance: ${self.current_user.capital:,.2f}{reset}")
                else:
                    print(f"{red}Failed to record closing transaction in database.{reset}")
            else:
                print(f"{yel}Closing cancelled.{reset}")

        except sqlite3.Error as e:
            print(f"{red}Database error while processing derivative closing: {e}")
            
    def get_user_portfolio(self):
        """
        Fetches the user's portfolio. Now handles both regular buy/sell and Long/Short positions.
        Returns: {symbol: (quantity, position_type)}
        """
        portfolio = {}
        cursor = self.con.cursor()
        try:
            # Fetch ALL non-closed orders (Buy, Sell, Long, Short)
            cursor.execute('''
                SELECT symbol, order_type, quantity, position_type 
                FROM orders 
                WHERE user_id = ? AND status != 'CLOSED'
            ''', (self.current_user.id,)) 
            
            all_orders = cursor.fetchall()
            
            for order in all_orders:
                symbol, order_type, quantity, position_type = order
                
                # The portfolio key must include the position type to distinguish between e.g.
                # "AAPL" (stocks) and "BTC-USD LONG" (derivative)
                # For BTC-USD derivatives we use symbol + position_type
                if symbol == DERIVATIVE_SYMBOL and position_type in ('LONG', 'SHORT'):
                    key = f"{symbol} {position_type}"
                else:
                    key = symbol # For regular stocks/ETFs

                if key not in portfolio:
                    portfolio[key] = [0, position_type] # [Quantity, position_type]
                
                # Aggregation of quantity for traditional assets
                if order_type == 'BUY':
                    portfolio[key][0] += quantity
                elif order_type == 'SELL':
                    portfolio[key][0] -= quantity
                # Long/Short orders are simpler; they represent a unique position closed via close_derivative_position

            # Filter out assets with zero or negative quantity (traditional netting)
            final_portfolio = {symbol: data for symbol, data in portfolio.items() if data[0] > 0 or data[1] in ('LONG', 'SHORT')}
            return final_portfolio
            
        except sqlite3.Error as e:
            print(f"{red}Database error while fetching portfolio: {e}")
            return {}

    def show_transaction_history(self):
        """
        Fetches and displays all executed and closed transactions for the current user.
        """
        cursor = self.con.cursor()
        try:
            # Fetch all orders, including those marked as 'CLOSED'
            cursor.execute('''
                SELECT order_id, symbol, order_type, position_type, quantity, price, timestamp, status
                FROM orders
                WHERE user_id = ? AND status IN ('EXECUTED', 'CLOSED')
                ORDER BY timestamp DESC
            ''', (self.current_user.id,))
        
            transactions = cursor.fetchall()

            print(f"\n{yel}{bold}*** Transaction History for {self.current_user.name} ***{reset}")
            print("-" * 90)
            
            if not transactions:
                print(f"{mag}No executed transactions found.{reset}")
                print("-" * 90)
                return

            # Define widths for columns
            col_widths = {
                'ID': 4,
                'TYPE': 6,
                'POS': 6,
                'QTY': 6,
                'SYMBOL': 8,
                'PRICE': 12,
                'TOTAL': 15,
                'STATUS': 8,
                'TIMESTAMP': 25
            }
            
            # Print header
            header = (
                f"{bold}{cyan}{'ID':<{col_widths['ID']}} | "
                f"{'TYPE':<{col_widths['TYPE']}} | "
                f"{'POS':<{col_widths['POS']}} | "
                f"{'QTY':<{col_widths['QTY']}} | "
                f"{'SYMBOL':<{col_widths['SYMBOL']}} | "
                f"{'PRICE':>{col_widths['PRICE']}} | "
                f"{'VALUE':>{col_widths['TOTAL']}} | "
                f"{'STATUS':<{col_widths['STATUS']}} | "
                f"{'TIMESTAMP':<{col_widths['TIMESTAMP']}}{reset}"
            )
            print(header)
            print("-" * 90)

            # Print transactions
            for tx in transactions:
                order_id, symbol, order_type, position_type, quantity, price, timestamp, status = tx
                
                total = quantity * price
                
                # Choose color based on transaction type and status
                if status == 'CLOSED':
                    tx_color = mag
                    status_str = "CLOSED"
                elif order_type == 'BUY' or order_type == 'LONG':
                    tx_color = green
                    status_str = "OPENED"
                elif order_type == 'SELL' or order_type == 'SHORT':
                    tx_color = red
                    status_str = "OPENED"
                else:
                    tx_color = reset
                    status_str = "EXEC"

                # Format transaction row
                tx_row = (
                    f"{order_id:<{col_widths['ID']}} | "
                    f"{order_type:<{col_widths['TYPE']}} | "
                    f"{position_type if position_type else '-':<{col_widths['POS']}} | "
                    f"{quantity:<{col_widths['QTY']}} | "
                    f"{cyan}{symbol:<{col_widths['SYMBOL']}}{reset} | "
                    f"{price:>{col_widths['PRICE']},.2f} | "
                    f"{tx_color}{total:>{col_widths['TOTAL']},.2f}{reset} | "
                    f"{status_str:<{col_widths['STATUS']}} | "
                    f"{timestamp:<{col_widths['TIMESTAMP']}}"
                )
                print(tx_row)
        except sqlite3.Error as e:
            print(f"{red}Database error while fetching transaction history: {e}")

            print("-" * 90)
            input(f"\n{blue}Press Enter to return to the Order Menu...{reset}") # Pause