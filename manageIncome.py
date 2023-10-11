import sqlite3
import tkinter
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from numpy import double
from numpy import *
from tkcalendar import DateEntry
import customtkinter
import database

amount = None
description = None
dt = None
root = None
def add_Income(amt,desc,date):
    global amount, description, dt
    amount = str(amt)
    description = desc
    dt = str(date)
    type='income'
    c= database.table()
    c.execute("select id from users where username = '"+unm+"'")
    user_id = str(c.fetchone()[0])
    print(amount ,description ,dt ,user_id)
    if amount == None or description == None:
        messagebox.showerror("Error", "Please Fill All Fields")
        return

    if amount == "" or description == "":
        messagebox.showerror("Error", "Please Fill All Fields")
        return


    if not amount.isdigit():
        messagebox.showinfo("Error", "please enter a number")
        return


    try:
        # c = database.table()
        # c.execute(''' Insert into transactions(user_id,type,amount,description,date) values (?,?,?,?,?)''',(user_id,'income',amount,description,date))
        data = database.add_transaction(user_id,type,amount,description,date)
        if data == True:
            messagebox.showinfo("Success", "Income Added")
    except Exception as e:
        print(e)
        messagebox.showerror("error", e)
        c.rollback()


def ManageIncome(Root):
    expenses_frame = customtkinter.CTkFrame(Root, corner_radius=0, fg_color="transparent")
    root = expenses_frame
    global unm
    unm= "user1234"

    income_label = tkinter.Label(root, text="Add Your Income", font=("Arial", 16), bg="#f5f5f5")
    income_label.pack(pady=10)

    income_frame = customtkinter.CTkFrame(root, width=320, height=360, corner_radius=15, bg_color='#f5f5f5')
    income_frame.pack(pady=10)

    dt = DateEntry(income_frame, date=datetime.today(), font=customtkinter.CTkFont(size=20, ), width=20,
                   )
    dt.place(x=65, y=45)

    amount = customtkinter.CTkEntry(income_frame, placeholder_text="Add Amount",
                                    font=customtkinter.CTkFont(size=20), width=200)
    amount.place(x=50, y=75)

    description = customtkinter.CTkEntry(income_frame, placeholder_text="Add Description",
                                         font=customtkinter.CTkFont(size=20), width=200)
    description.place(x=50, y=130)

    button = customtkinter.CTkButton(income_frame, text="Add Income",
                                     font=customtkinter.CTkFont(size=20, weight="bold"), width=200,
                                     command=lambda: add_Income(amount.get(),description.get(),dt.get_date()))
    button.place(x=50, y=185)

    return expenses_frame