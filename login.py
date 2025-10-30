#AlgoDesk 2025 Mallard-Dash
#login.py

from users import User 
import os
import time
import sqlite3
import pwinput
import textual_dev as tx
from colorama import Fore, init
init()

# Constants
MAX_USERNAME_LENGTH = 50
SLEEP_DURATION = 2
MENU_OPTIONS = {
    "1": "Log in existing user",
    "2": "Create new user", 
    "3": "Exit"
}

# Database queries
SELECT_USER_QUERY = "SELECT name, email, password, capital FROM USERS WHERE name = ?"

# Tell the program where to put the database-file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")

# Disclaimer text as constant
DISCLAIMER_TEXT = f"""{Fore.RED}===================================================================
                 AlgoDesk - Terms of Use & Disclaimer                 
===================================================================

{Fore.YELLOW}1. No Financial Advice
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
By typing "Agree" or by using this Program, you acknowledge that
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
    print("*** LOGIN PAGE ***")
    username = input("Username: ").strip()
    password = pwinput.pwinput(prompt="Password: ", mask='*')

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_USER_QUERY, (username,))
            user_data = cursor.fetchone()
            
            # Check if user exists and password matches
            if user_data and user_data[2] == password:  # user_data[2] is the password
                print(f"Welcome, {user_data[0]}!")  # user_data[0] is the name
                
                # Create the User object with the data from the database
                user_session = User(
                    name=user_data[0], 
                    email=user_data[1], 
                    password=user_data[2], 
                    capital=user_data[3]
                )
                return user_session  # SUCCESS! Return the entire object
            else:
                print("Invalid username or password.")
                return None  # FAILURE! Return None
                
    except sqlite3.Error as database_error:
        print(f"Database error: {database_error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return None


def show_login_menu():
    """
    Display the main login menu and handle user navigation.
    
    Returns:
        User: Authenticated user object if login successful
        False: If user chooses to exit or agreement declined
    """
    if not disclaimer():
        print(Fore.RED + "To use this program you need to agree on the user-terms!")
        time.sleep(SLEEP_DURATION)
        return False

    while True:
        try:
            print(f"\n***AlgoDesk-Login-Menu***\n"
                  f"1. {MENU_OPTIONS['1']}\n"
                  f"2. {MENU_OPTIONS['2']}\n"
                  f"3. {MENU_OPTIONS['3']}")
            
            menu_choice = input("Please choose a menu choice: ").strip()
            
            match menu_choice:
                case "1":
                    # user_object will be the User object or None
                    user_object = login_existing_user() 
                    if user_object is not None:
                        return user_object  # Pass the User object up to main.py
                
                case "2":
                    try:
                        new_user_obj = User()
                        new_user_obj.new_user() 
                    except Exception as e:
                        print(f"Error creating new user: {e}")
                    continue 
                
                case "3":
                    print("Turning off...Bye")
                    time.sleep(SLEEP_DURATION)
                    return False  # Tell main.py to quit
                
                case _:
                    print("Invalid choice. Please select 1, 2, or 3.")
                    
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred in menu: {e}")


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
            conditions = input(f"{Fore.WHITE}If you accept the terms, type {Fore.GREEN}AGREE.{Fore.WHITE} If not, type {Fore.RED}EXIT: {Fore.RESET}")
            
            # Standardize the input
            clean_input = conditions.upper().strip()
            
            if clean_input == "AGREE":
                return True  # Exit the loop and return True
            elif clean_input == "EXIT":
                return False  # Exit the loop and return False
            else:
                # This will re-run the loop
                print(Fore.RED + "Invalid input. Please type 'AGREE' or 'EXIT'.\n")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            return False
        except Exception as e:
            print(f"Error in disclaimer: {e}")
            return False