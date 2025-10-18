#AlgoDesk 2025 Mallard-Dash
#users.py

import time
import datetime
import sqlite3
import random
import os
import pwinput

#Tell the program where to put the database-file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")


#Connect to database
con = sqlite3.connect(DB_PATH)

class User:
    def __init__(self, password = None, email = None, name = None, capital = 0, currency = None):
        self.name = name
        self.capital = capital
        self.currency = currency
        self.password = password
        self.email = email

    def new_user(self):

        while True:

            self.name = input("Enter your username: ")
            if self.check_if_name_is_taken() == False:
                print("This username is already in use!")
                continue
            else:
                print("Name OK")

            self.email = input("Enter your email: ")
            if self.check_if_email_is_taken() == False:
                print("This email is already in use!")
                continue
            else:
                print("Email OK")

            if self.password_is_ok() == False:
                continue
            else:
                print("Password OK!")
                account_no = self.generate_account_number()
                capital = 100000

                data = (self.name, self.email, self.password, account_no, capital)
                cur = con.cursor()
                cur.execute("INSERT INTO USERS VALUES(?,?,?,?,?)",data)
                con.commit()
                print(f"User {self.name} created!")
                return



    def generate_account_number(self):
        while True:
            account_no = (random.randint(100,999))
            cur = con.cursor()
            cur.execute("SELECT account_no FROM Users WHERE account_no = ?", (account_no,))
            account_no_exist_not = cur.fetchone()

            if account_no_exist_not == None:
                return account_no
            else:
                continue

    def check_if_name_is_taken(self):
        cur = con.cursor()
        cur.execute("SELECT name FROM Users WHERE name = ?", (self.name, ))
        name_exist = cur.fetchone()

        if name_exist == None:
            return True #True means that it does not exist a user with that name = Green light
        else:
            return False #RED light

    def check_if_email_is_taken(self):
        cur = con.cursor()
        cur.execute("SELECT email FROM Users WHERE email = ?", (self.email, ))
        result_is_notning = cur.fetchone()


        if result_is_notning == None:
            return True #= GREEN light
        else: 
            return False #False means that we can't add another user with the same name = RED light

    def password_is_ok(self):
        self.password = pwinput.pwinput(prompt="Enter a password: ", mask='*')
        pwd_check = pwinput.pwinput(prompt="Enter the same password again: ", mask='*')
        pwd_match = False
                
        if self.password != pwd_check:
            pwd_match = False
            return False
        elif self.password == pwd_check:
            return self.password


    def check_user_balance(self):
        while True:
            print(f"Checking balance for {self.name}...")
            time.sleep(1.5)
            cur = con.cursor()
            cur.execute("SELECT capital FROM Users WHERE name = ?", (self.name, ))
            result = cur.fetchone()
            if result:
                print(f"Your balance is {result[0]} SEK")
                input("Press ENTER to return to main-menu...")
                return
            else:
                print("Error! Could not get balance.")
                return

    def logout_user():
        pass

    def user_session():
        pass

    def show_user_account_amount():
        pass

    def is_logged_in():
        pass

    def can_afford_derivate():
        pass
