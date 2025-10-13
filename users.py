#AlgoDesk 2025 Mallard-Dash
#users.py

import time
import datetime
import sqlite3

class User:
    def __init__(self, name = None, capital = 0, currency = None):
        self.name = name
        self.capital = capital
        self.currency = currency

    def new_user(self, user):
        user = self.name
        "SEK" = self.currency
        self.capital += 100000


def store_user_in_db():
    pass

def check_user_balance():
    pass

def login_user():
    pass

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
