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

#Tell the program where to put the database-file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")


def login_existing_user():
    print("*** LOGIN PAGE ***")
    name = input("Username: ")
    password = pwinput.pwinput(prompt="Password: ", mask='*')

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    # Fetch the user's data to create an object
    cur.execute("SELECT name, email, password, capital FROM USERS WHERE name = ?", (name,))
    result = cur.fetchone()
    
    # Check if user exists and password matches
    if result and result[2] == password: # result[2] is the password
        print(f"Welcome, {result[0]}!")# result[0] is the name
        
        # Create the User object with the data from the database
        user_session = User(
            name=result[0], 
            email=result[1], 
            password=result[2], 
            capital=result[3]
        )
        con.close()
        return user_session  # <-- SUCCESS! Return the *entire object*
    else:
        print("Invalid username or password.")
        con.close()
        return None # <-- FAILURE! Return None

def show_login_menu():
    if not disclaimer():
        print(Fore.RED + "To use this program you need to agree on the user-terms!")
        time.sleep(2)
        return False

    while True:
            print("\n***AlgoDesk-Login-Menu***\n",
            "1. Log in existing user\n",
            "2. Create new user\n",
            "3. Exit")
            menu_choice = input("Please choose a menu choice: ")
            
            match menu_choice:
                case "1":
                    # user_object will be the User object or None
                    user_object = login_existing_user() 
                    if user_object is not None:
                        return user_object  # <-- Pass the User object up to main.py
                
                case "2":
                    new_user_obj = User()
                    new_user_obj.new_user() 
                    continue 
                
                case "3":
                    print ("Turning off...Bye")
                    time.sleep(2)
                    return False # <-- Tell main.py to quit
        
        

def disclaimer():
        print(
        f"{Fore.RED}===================================================================\n"
        "                 AlgoDesk - Terms of Use & Disclaimer                 \n"
        "===================================================================\n\n"
        f"{Fore.YELLOW}1. No Financial Advice\n"
        "   This software, \"AlgoDesk\" (the \"Program\"), is provided for educational and\n"
        "   informational purposes only. The Program and all content provided by its\n"
        "   creator(s) do not constitute financial, investment, legal, or tax advice.\n"
        "   The creator of this Program is not a registered financial advisor or professional.\n\n"
        "2. Simulation Only\n"
        "   This Program is a paper trading simulator. All capital, assets, and \n"
        "   transactions are fictitious. Any resemblance to real-world market \n"
        "   performance is for simulation purposes. No real money is being used.\n\n"
        "3. No Guarantee of Performance\n"
        "   The results of simulated trading in this Program are not an indicator of\n"
        "   future results in a live trading environment. Simulated performance does\n"
        "   not account for real-world market factors such as liquidity, slippage,\n"
        "   or order execution speed.\n\n"
        "4. Assumption of Risk\n"
        "   All financial trading, real or simulated, involves risk. You, the user,\n"
        "   acknowledge that you understand these risks. Any trading strategies you\n"
        "   test or develop using this Program are used at your own sole risk.\n\n"
        "5. Limitation of Liability & \"As-Is\"\n"
        "   This Program is provided \"AS IS\" without any warranties. The creator of\n"
        "   this Program shall not be liable for any direct, indirect, or consequential\n"
        "   losses, damages, or costs arising from your use of, or inability to use,\n"
        "   this Program. This includes any financial losses you may incur in your\n"
        "   real-world trading activities, even if they are based on strategies or\n"
        "   information from this Program.\n\n"
        "-------------------------------------------------------------------\n"
        "By typing \"Agree\" or by using this Program, you acknowledge that\n"
        "you have read, understood, and agree to be bound by these terms.\n"
        "-------------------------------------------------------------------\n")

    # This loop will run until the user gives a valid answer
        while True: 
            conditions = input(f"{Fore.WHITE}If you accept the terms, type {Fore.GREEN}AGREE.{Fore.WHITE} If not, type {Fore.RED}EXIT: {Fore.RESET}")
            
            # Standardize the input
            clean_input = conditions.upper() 
            
            if clean_input == "AGREE":
                return True  # Exit the loop and return True
            elif clean_input == "EXIT":
                return False # Exit the loop and return False
            else:
                # This will re-run the loop
                print(Fore.RED + "Invalid input. Please type 'AGREE' or 'EXIT'.\n")