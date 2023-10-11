import sqlite3
from datetime import datetime

global conn,c
conn = sqlite3.connect('Expense_Tracker')
c = conn.cursor()

def table():

    c.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE,
               email TEXT,
               password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       user_id INTEGER,
                                       type Text,
                                       amount Double,
                                       description TEXT,
                                       date TEXT
                                      )''')
    conn.commit()
    return c

def get_transactions():
    try:
        c.execute('''SELECT * FROM Transactions''')
        data = c.fetchall()
        return data
    except Exception as e:
        return e

def add_transaction(user_id, type, amount, description, date):
    try:
        c.execute('''INSERT INTO Transactions (user_id, type, amount, description, date) VALUES (?,?,?,?,?)''', (user_id, type, amount, description, date))
        conn.commit()
        return True
    except Exception as e:
        return e

def update_transaction(user_id, type, amount, description, date):
    try:
        c.execute('''UPDATE Transactions SET type =?, amount =?, description =?, date =? WHERE user_id =?''', (type, amount, description, date, user_id))
        conn.commit()
        return True
    except Exception as e:
        return e

def add_user(username, email, password):
    try:
        c.execute('''INSERT INTO users (username, email, password) VALUES (?,?,?)''', (username, email, password))
        conn.commit()
        return True
    except Exception as e:
        return e


def login(username, password):
    username= username
    password= password
    try:
        c.execute('''SELECT * FROM users WHERE username =? AND password =?''', (username, password))
        conn.commit()
        data = c.fetchone()
        return True
    except Exception as e:
        return e
