#AlgoDesk 2025 Mallard-Dash
#login.py (Revised with unified color style)

from users import User 
import os
import time
import sqlite3
import pwinput
# import textual_dev as tx # Not used in this file
from colorama import Fore, Style, init
init(autoreset=True) # Use autoreset=True to match other files

# --- Color Setup ---
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW
cyan = Fore.CYAN
bold = Style.BRIGHT
reset = Style.RESET_ALL

# Constants
MAX_USERNAME_LENGTH = 50
SLEEP_DURATION = 2
MENU_OPTIONS = {
    "1": "Log in existing user",
    "2": "Create new user", 
    "3": "Exit"
}

# Database queries
SELECT_USER_QUERY = "SELECT account_id, name, email, password, capital FROM Users WHERE name = ?"

# Tell the program where to put the database-file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")

# Disclaimer text as constant (Updated colors here for consistency)
DISCLAIMER_TEXT = f"""{red}===================================================================
                 {bold}AlgoDesk - Terms of Use & Disclaimer{reset}{red}                 
===================================================================

{yel}1. No Financial Advice
   This software, "AlgoDesk" (the "Program"), is provided for educational and
   informational purposes only. The Program and all content provided by its
   creator(s) do not constitute financial, investment, legal, or tax advice.
   The creator of this Program is not a registered financial advisor or professional.

2. Simulation Only
   This Program is a paper trading simulator. All capital, assets, and 
   transactions are fictitious. Any resemblance to real-world market 
   performance is for simulation purposes. No real money is being used.

3. No Guarantee of Performance
   The results of simulated trading in this Program are not an indicator of
   future results in a live trading environment. Simulated performance does
   not account for real-world market factors such as liquidity, slippage,
   or order execution speed.

4. Assumption of Risk
   All financial trading, real or simulated, involves risk. You, the user,
   acknowledge that you understand these risks. Any trading strategies you
   test or develop using this Program are used at your own sole risk.

5. Limitation of Liability & "As-Is"
   This Program is provided "AS IS" without any warranties. The creator of
   this Program shall not be liable for any direct, indirect, or consequential
   losses, damages, or costs arising from your use of, or inability to use,
   this Program. This includes any financial losses you may incur in your
   real-world trading activities, even if they are based on strategies or
   information from this Program.

-------------------------------------------------------------------
By typing "{green}{bold}AGREE{reset}{yel}" or by using this Program, you acknowledge that
you have read, understood, and agree to be bound by these terms.
-------------------------------------------------------------------
"""


def login_existing_user():
    """
    Authenticate an existing user by username and password.
    
    Returns:
        User: User object if authentication successful
        None: If authentication fails or error occurs
    """
    print(f"\n{cyan}*** LOGIN PAGE ***{reset}")
    username = input(f"{blue}Username: {reset}").strip()
    password = pwinput.pwinput(prompt=f"{blue}Password: {reset}", mask='*')

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_USER_QUERY, (username,))
            user_data = cursor.fetchone()

            if user_data and user_data[3] == password:
                # Success feedback
                print(f"\n{green}{bold}✅ Welcome, {user_data[1]}! Logging in...{reset}")
                time.sleep(1)
                user_session = User(
                    user_id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password=user_data[3],
                    capital=user_data[4]
                )
                return user_session
            else:
                # Failure feedback
                print(f"\n{red}❌ Invalid username or password.{reset}")
                time.sleep(SLEEP_DURATION)
                return None
    except sqlite3.Error as database_error:
        print(f"{red}Database error: {database_error}{reset}")
        time.sleep(SLEEP_DURATION)
        return None
    except Exception as e:
        print(f"{red}An unexpected error occurred during login: {e}{reset}")
        time.sleep(SLEEP_DURATION)
        return None


def show_login_menu():
    """
    Display the main login menu and handle user navigation.
    
    Returns:
        User: Authenticated user object if login successful
        False: If user chooses to exit or agreement declined
    """
    if not disclaimer():
        print(f"\n{red}{bold}To use this program you need to agree on the user-terms!{reset}")
        time.sleep(SLEEP_DURATION)
        return False

    while True:
        try:
            print(f"\n{mag}=" * 30)
            print(f"{mag}{bold}*** AlgoDesk Login Menu ***{reset}")
            print(f"{mag}=" * 30)
            
            # Nicer menu printout
            print(f"{cyan}1. {reset}{bold}{MENU_OPTIONS['1']}{reset}")
            print(f"{cyan}2. {reset}{bold}{MENU_OPTIONS['2']}{reset}")
            print(f"{cyan}3. {red}{bold}{MENU_OPTIONS['3']}{reset}")
            print("-" * 30)
            
            menu_choice = input(f"{blue}{bold}➤ Please choose an option (1-3): {reset}").strip()
            
            match menu_choice:
                case "1":
                    user_object = login_existing_user() 
                    if user_object is not None:
                        return user_object
                
                case "2":
                    print(f"\n{green}{bold}*** Create New User ***{reset}")
                    try:
                        new_user_obj = User()
                        new_user_obj.new_user() 
                        print(f"{green}Account successfully created. Please log in.{reset}")
                    except Exception as e:
                        print(f"{red}Error creating new user: {e}{reset}")
                    time.sleep(SLEEP_DURATION)
                    continue 
                
                case "3":
                    print(f"{yel}Turning off... Bye!{reset}")
                    time.sleep(SLEEP_DURATION)
                    return False
                
                case _:
                    print(f"{red}Invalid choice. Please select 1, 2, or 3.{reset}")
                    
        except KeyboardInterrupt:
            print(f"\n\n{yel}Program interrupted by user. Exiting.{reset}")
            return False
        except Exception as e:
            print(f"{red}An unexpected error occurred in menu: {e}{reset}")


def disclaimer():
    """
    Display terms of service and get user agreement.
    
    Returns:
        bool: True if user agrees to terms, False otherwise
    """
    print(DISCLAIMER_TEXT)

    # This loop will run until the user gives a valid answer
    while True:
        try:
            # Clearer prompt
            conditions = input(f"{bold}{yel}Accept terms? ({green}AGREE{yel}/{red}EXIT{yel}): {reset}")
            
            clean_input = conditions.upper().strip()
            
            if clean_input == "AGREE":
                print(f"\n{green}Agreement accepted. Proceeding to login menu...{reset}")
                time.sleep(1)
                return True
            elif clean_input == "EXIT":
                print(f"\n{red}Agreement declined. Exiting program.{reset}")
                return False
            else:
                print(f"{red}Invalid input. Please type '{green}AGREE{red}' or '{red}EXIT{red}'.{reset}\n")
                
        except KeyboardInterrupt:
            print(f"\n\n{yel}Program interrupted by user. Exiting.{reset}")
            return False
        except Exception as e:
            print(f"{red}Error in disclaimer: {e}{reset}")
            return False