#users.py 

import time
import datetime
import sqlite3
import random
import os
import pwinput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")

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


class User:
    def __init__(self, user_id: int = None, name: str = None, email: str = None,
                 password: str = None, capital: float = 0.0, currency: str = "USD"): # Default till USD
        # user_id maps to DB column account_id; keep .id for compatibility
        self.id = user_id
        self.account_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.capital = float(capital or 0.0)
        self.currency = currency

    def new_user(self):
        while True:
            self.name = input("Enter your username: ").strip()
            if not self.check_if_name_is_taken():
                print(f"{red}This username is already in use!{reset}")
                continue
            else:
                print(f"{green}Name OK{reset}")

            self.email = input("Enter your email: ").strip()
            if not self.check_if_email_is_taken():
                print(f"{red}This email is already in use!{reset}")
                continue
            else:
                print(f"{green}Email OK{reset}")

            if not self.password_is_ok():
                continue
            else:
                print(f"{green}Password OK!{reset}")
                account_id = self.generate_account_number()
                capital = 10000.00  # starting capital 

                data = (account_id, self.name, self.email, self.password, capital)
                sql_query = """
                INSERT INTO Users (account_id, name, email, password, capital) 
                VALUES (?, ?, ?, ?, ?);
                """
                with sqlite3.connect(DB_PATH) as conn:
                    cur = conn.cursor()
                    cur.execute(sql_query, data)
                    conn.commit()
                print(f"{green}User {self.name} created! Starting Capital: ${capital:,.2f}{reset}")
                return

    def generate_account_number(self):
        while True:
            account_id = random.randint(100000, 999999)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("SELECT account_id FROM Users WHERE account_id = ?", (account_id,))
                if cur.fetchone() is None:
                    return account_id

    def check_if_name_is_taken(self):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM Users WHERE name = ?", (self.name,))
            return cur.fetchone() is None

    def check_if_email_is_taken(self):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT email FROM Users WHERE email = ?", (self.email,))
            return cur.fetchone() is None

    def password_is_ok(self):
        self.password = pwinput.pwinput(prompt="Enter a password: ", mask='*')
        pwd_check = pwinput.pwinput(prompt="Enter the same password again: ", mask='*')
        if self.password != pwd_check:
            print(f"{red}Passwords do not match.{reset}")
            return False
        return True

    def get_capital_from_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT capital FROM Users WHERE account_id = ?", (self.id,))
            result = cur.fetchone()
            if result:
                self.capital = float(result[0])
                return self.capital
            else:
                print(f"{red}Error! Could not find account balance.{reset}")
                return None

    def check_user_balance(self):
        current_capital = self.get_capital_from_db()
        if current_capital is not None:
            print(f"\n{cyan}*** Account Balance ***{reset}")
            print(f"{bold}Account ID:{reset} {self.id}")
            print(f"{bold}Available Capital:{reset} {green}${current_capital:,.2f} {self.currency}{reset}")
            print("-------------------------")
        input(f"\n{blue}Press ENTER to return to the Balance Menu...{reset}")
        return current_capital

    def update_user_balance(self, new_balance):
        return self.save_balance(new_balance)

    def save_balance(self, new_balance):
        """Persist new balance to DB and update self.capital."""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("UPDATE Users SET capital = ? WHERE account_id = ?", (new_balance, self.id))
                conn.commit()
            self.capital = float(new_balance)
            return True
        except sqlite3.Error as e:
            print(f"{red}Database error while updating balance: {e}{reset}")
            return False

    def save(self, con: sqlite3.Connection | None = None):
        """
        Persist current user capital (self.capital) to DB using account_id column.
        """
        close_conn = False
        if con is None:
            con = sqlite3.connect(DB_PATH)
            close_conn = True
        try:
            cur = con.cursor()
            cur.execute("UPDATE Users SET capital = ? WHERE account_id = ?", (self.capital, self.id))
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"{red}Failed to save user capital: {e}{reset}")
            return False
        finally:
            if close_conn:
                con.close()


    def show_balance_menu(self):
        """Huvudmeny för att hantera insättningar och uttag."""
        while True:
            self.get_capital_from_db() 
            
            print(f"\n{mag}=" * 35)
            print(f"{mag}{bold}*** Capital Management Menu ***{reset}")
            print(f"{mag}=" * 35)
            print(f"{yel}Current Capital: ${self.capital:,.2f} {self.currency}{reset}")
            print("-" * 35)
            print(f"{cyan}1. {reset}View current balance")
            print(f"{cyan}2. {reset}{green}Deposit Funds{reset}")
            print(f"{cyan}3. {reset}{red}Withdraw Funds{reset}")
            print(f"{cyan}4. {reset}Exit to main menu")
            print("-" * 35)

            menu_choice = input(f"{blue}{bold}➤ Choose an option (1-4): {reset}").strip()

            match menu_choice:
                case "1":
                    self.check_user_balance()
                case "2":
                    self.deposit_funds()
                case "3":
                    self.withdraw_funds()
                case "4":
                    print(f"{yel}Returning to main menu...{reset}")
                    break
                case _:
                    print(f"{red}Invalid choice, please try again.{reset}")
    
    def deposit_funds(self):
        """Hanterar insättning av kapital."""
        print(f"\n{green}{bold}*** Deposit Funds ***{reset}")
        print(f"Current Capital: ${self.capital:,.2f} {self.currency}")
        
        try:
            amount_input = input(f"{blue}Enter amount to deposit (e.g., 5000.00): ${reset}").strip()
            amount = float(amount_input)
        except ValueError:
            print(f"{red}Invalid amount. Please enter a valid number.{reset}")
            return

        if amount <= 0:
            print(f"{red}Deposit amount must be positive.{reset}")
            return

        new_balance = self.capital + amount
        
        if self.save_balance(new_balance):
            print(f"\n{green}{bold}✅ Deposit successful!{reset}")
            print(f"{green}Deposited: ${amount:,.2f}{reset}")
            print(f"{green}New Capital: ${new_balance:,.2f} {self.currency}{reset}")
        else:
            print(f"{red}Deposit failed due to a database error.{reset}")

    def withdraw_funds(self):
        """Hanterar uttag av kapital."""
        print(f"\n{red}{bold}*** Withdraw Funds ***{reset}")
        print(f"Current Capital: ${self.capital:,.2f} {self.currency}")

        try:
            amount_input = input(f"{blue}Enter amount to withdraw: ${reset}").strip()
            amount = float(amount_input)
        except ValueError:
            print(f"{red}Invalid amount. Please enter a valid number.{reset}")
            return

        if amount <= 0:
            print(f"{red}Withdrawal amount must be positive.{reset}")
            return
            
        if amount > self.capital:
            print(f"{red}Insufficient funds. You can only withdraw up to ${self.capital:,.2f}.{reset}")
            return

        new_balance = self.capital - amount
        
        if self.save_balance(new_balance):
            print(f"\n{green}{bold}✅ Withdrawal successful!{reset}")
            print(f"{red}Withdrew: ${amount:,.2f}{reset}")
            print(f"{green}New Capital: ${new_balance:,.2f} {self.currency}{reset}")
        else:
            print(f"{red}Withdrawal failed due to a database error.{reset}")