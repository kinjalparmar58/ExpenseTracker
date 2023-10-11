import tkinter
from tkinter import messagebox

import customtkinter
from tkinter import *
import sqlite3
import database
import home


class Login(customtkinter.CTk):
    APP_NAME = "Expense Tracker "
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Login.APP_NAME)
        self.geometry(str(Login.WIDTH) + "x" + str(Login.HEIGHT))
        self.minsize(Login.WIDTH, Login.HEIGHT)
        self.maxsize(Login.WIDTH, Login.HEIGHT)
        self.resizable(False, False)
        # self.iconname("assets/budget.png")
        # creating login frame
        frame = customtkinter.CTkFrame(
            master=self, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        lable_1 = customtkinter.CTkLabel(
            master=frame, text="Log into your Account", font=('Century Gothic', 20))
        lable_1.place(x=50, y=45)

        self.username_entry = customtkinter.CTkEntry(
            master=frame, width=220, placeholder_text='Username')
        self.username_entry.place(x=50, y=110)

        self.password_entry = customtkinter.CTkEntry(
            master=frame, width=220, placeholder_text='Password', show="*")
        self.password_entry.place(x=50, y=165)

        label2 = customtkinter.CTkLabel(
            master=frame, text="Forget password?", font=('Century Gothic', 12))
        label2.place(x=155, y=195)

        # Create login button
        self.login_button = customtkinter.CTkButton(
            master=frame, width=220, text="Login", command=self.create_login, corner_radius=6)
        self.login_button.place(x=50, y=240)

        self.reg_button = customtkinter.CTkButton(
            master=frame, width=220, text="Register", command=self.register, corner_radius=6)
        self.reg_button.place(x=50, y=280)

        self.errorLabel = customtkinter.CTkLabel(frame, width=220, text_color="red",text="", corner_radius=6)
        self.errorLabel.place(x=50, y=340)

        print(tkinter.TkVersion)

    def create_login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()


            if username == '' or password == '':
                self.errorLabel.configure(text="Please fill all fields")
                return
            try:
                c = database.table()
                c.execute("SELECT * FROM users WHERE username =? and password = ?", (username, password))
                data = c.fetchone()
                if data == None:
                    self.errorLabel.configure(text="Invalid login credentials")
                    messagebox.showinfo('Error', 'Invalid login credentials')
                else:
                    # messagebox.showinfo('Success', 'logged in successfully')
                    self.destroy()
                    app = home.Dashboard(username)
                    app.mainloop()
            except Exception as e:
                    print('Error :', e)

    def register(self):
        self.destroy()
        import add_user
        app = add_user.Add_User()
        app.mainloop()

if __name__ == "__main__":
    app = Login()
    app.mainloop()
