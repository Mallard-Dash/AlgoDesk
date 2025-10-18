#AlgoDesk 2025 Mallard-Dash
#login.py


from users import User 
import os
import time
import sqlite3
import pwinput

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
        print(f"Welcome, {result[0]}!") # result[0] is the name
        
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
                new_user_obj = User.new_user() 
                continue 
            
            case "3":
                print ("Turning off...Bye")
                time.sleep(2)
                return False # <-- Tell main.py to quit