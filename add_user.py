from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
import re

import customtkinter

import database
import login_screen

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")

class Add_User(customtkinter.CTk):
    APP_NAME = "Expense Tracker "
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Add_User.APP_NAME)
        self.geometry(str(Add_User.WIDTH) + "x" + str(Add_User.HEIGHT))
        self.minsize(Add_User.WIDTH, Add_User.HEIGHT)
        self.maxsize(Add_User.WIDTH, Add_User.HEIGHT)
        self.resizable(False, False)

        # creating login frame
        self.frame = customtkinter.CTkFrame(
            master=self, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

        lable_1 = customtkinter.CTkLabel(
            master=self.frame, text="Wellcome to Expense Tracker", font=('Century Gothic', 20))
        lable_1.pack(pady=10,padx=10)

        self.email = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Email", width=220
        )
        self.email.pack(pady=10, padx=10)

        self.username = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Username", width=220

        )
        self.username.pack(pady=10, padx=10)

        self.password = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Password",
            show="*", width=220
        )
        self.password.pack(pady=10, padx=10)

        self.c_pass = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Confirm Password",
            show="*", width=220
        )
        self.c_pass.pack(pady=10, padx=10)

        self.button = customtkinter.CTkButton(
            self.frame, width=220, text="Add User", command=self.register_user, corner_radius=6
        )
        self.button.pack(pady=10, padx=10)

        self.mainloop()

    def register_user(self):
        email = self.email.get()
        username = self.username.get()
        password = self.password.get()
        confirm_password = self.c_pass.get()

        # check for empty fields
        if not email or not username or not password or not confirm_password:
            messagebox.showerror('Error', 'Please fill in all fields')
            return

            # check email format
        if not re.match(r'^\S+@\S+\.\S+$', email):
            messagebox.showerror('Error', 'Invalid email format')
            self.email.focus()
            return

            # check password length
        if len(password) < 8:
            messagebox.showerror('Error', 'Password must be at least 8 characters')
            self.password.focus()
            return

            # check if passwords match
        if password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match')
            self.c_pass.focus()
            return

            # insert user data into database
        try:
            dt = database.add_user(username, email, password)
            if dt == True:
                messagebox.showinfo('Success', 'User registered successfully')
                Add_User.destroy(self)
                app=login_screen.Login()
                app.mainloop()
            else:
                print(dt)
                messagebox.showerror('Error', 'User registration failed')
        except sqlite3.IntegrityError:
            messagebox.showerror('Error', 'Email or username already exists')
            return

if __name__ == "__main__":
    app =  Add_User()
    app.mainloop()