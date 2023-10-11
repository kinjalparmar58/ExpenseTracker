import datetime
from tkinter import messagebox
import dataVisualize
import login_screen
import customtkinter
import database
from manageExpense import ManageExpense

income = None
expense = None


class Recent_Transaction(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.date_label = []
        self.disc_label = []
        self.amount_label = []

    def add_item(self, date, amount,disc):
        label1 = customtkinter.CTkLabel(self, text=date, compound="left", padx=5, anchor="w")
        label2 = customtkinter.CTkLabel(self, text=disc,  compound="left", padx=5, anchor="w")
        label3 = customtkinter.CTkLabel(self, text=amount, compound="left", padx=5, anchor="w")

        label1.grid(row=len(self.date_label), column=0, pady=(0, 10), sticky="w")
        label2.grid(row=len(self.disc_label), column=1, pady=(0, 10), padx=5)
        label3.grid(row=len(self.amount_label), column=2, pady=(0, 10), padx=5)
        self.date_label.append(label1)
        self.disc_label.append(label2)
        self.amount_label.append(label3)


class Dashboard(customtkinter.CTk):
    APP_NAME = "Expense Tracker"
    WIDTH = 700
    HEIGHT = 550

    def __init__(self,username, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Expense Tracker")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.username = username
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0,  padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Dashboard",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   anchor="w",
                                                   command=self.home_button_event
                                                   )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.income = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Manage_Income",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                       anchor="w",
                                                      command=self.income_button_event
                                              )
        self.income.grid(row=2, column=0, sticky="ew")
        self.expense = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, text="Manage_Expense",
                                              fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              anchor="w",
                                              command=self.expense_button_event
                                              )
        self.expense.grid(row=3, column=0, sticky="ew")


        self.history = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="History",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w",
                                                      command=self.history_click_command
                                               )
        self.history.grid(row=4, column=0, sticky="ew")

        self.visualization = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Data_Visualization",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w",
                                                      command=self.visualization_click_command
                                                     )
        self.visualization.grid(row=5, column=0, sticky="ew")

        self.appearance_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Theme:", anchor="w"
        )
        self.appearance_label.grid(row=7, column=0, padx=20,pady=(5, 0) )
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event
                                                                )
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        self.scaling_label = customtkinter.CTkLabel(
            self.navigation_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        self.logout =customtkinter.CTkButton(self.navigation_frame,text="Logout",corner_radius=20, height=40,
                                                      border_spacing=20,
                                                      fg_color="transparent", text_color=("gray10", "RED"),
                                                      font=customtkinter.CTkFont(size=15, weight="bold" ),
                                                      hover_color=("gray70", "darkred"),
                                                      anchor="w",
                                                      command=self.logout)
        self.logout.grid(row=11, column=0, padx=20, pady=(10, 20))

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.home_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.home_frame.grid_rowconfigure(2, weight=0)



        # Cards Frame

        income_card = customtkinter.CTkFrame(self.home_frame, width=500, corner_radius=0, bg_color='transparent')
        income_card.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 20))
        income_card.rowconfigure(2, weight=100)
        income_label = customtkinter.CTkLabel(income_card, text="Income", width=180,
                                               font=customtkinter.CTkFont(size=20,), text_color="#000000")
        income_label.grid(column=2, row=0)
        self.update_income()
        i_amt = customtkinter.CTkLabel(income_card, text="$"+str(income), font=customtkinter.CTkFont(size=25, weight="bold"),
                                       text_color="#000000",height=90)
        i_amt.grid(column=2, row=1)

        Expense_card = customtkinter.CTkFrame(self.home_frame, width=500, corner_radius=0, bg_color='transparent')
        Expense_card.grid(row=0, column=2, sticky="nsew", padx=10, pady=(10, 20))
        Expense_card.rowconfigure(2, weight=100)
        Expense_label = customtkinter.CTkLabel(Expense_card, text="Expense", width=180,
                                               font=customtkinter.CTkFont(size=20,), text_color="#000000")
        Expense_label.grid(column=2, row=0)
        self.update_expense()
        e_amt = customtkinter.CTkLabel(Expense_card, text="$"+str(expense), font=customtkinter.CTkFont(size=25, weight="bold"),
                                       text_color="#000000",height=90)
        e_amt.grid(column=2, row=1)

             #Recent transactions Frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="Recent Transactions")
        self.scrollable_frame.grid(row=2, column=1,columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.recent_transactions()

        #Bottom frame
        self.bottom_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0,height=90)
        self.bottom_frame.grid(row=3,column=0,columnspan=3, padx=(20,0),pady=(20,20), sticky="nsew")
        # self.bottom_frame.pack(side="bottom")
        user_lable = customtkinter.CTkButton(self.bottom_frame, corner_radius=2, height=10,
                                                      border_spacing=10, text=self.username,
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w",
                                                     )

        user_lable.pack(side="left")
        time_lable = customtkinter.CTkButton(self.bottom_frame, corner_radius=2, height=10,
                                             border_spacing=10, text=datetime.datetime.now(),
                                             fg_color="transparent", text_color="#618bff",
                                             hover_color=("gray70", "gray30"),
                                             anchor="w",
                                             )
        time_lable.pack(side="right")


        from manageIncome import ManageIncome
        self.income_frame = ManageIncome(self)
        self.expense_frame = ManageExpense(self)
        from historyframe import trancHistory
        self.history_frame = trancHistory(self)
        self.visualization_frame = dataVisualize.IncomeExpensePieChart(self)

    def update_income(self):
        global income
        try:
            c = database.table()
            c.execute("select SUM(amount) from transactions where type='income' ")
            income = c.fetchone()[0]
        except Exception as e:
            print(e)
        return income

    def update_expense(self):
        global expense
        try:
            c = database.table()
            c.execute("select SUM(amount) from transactions where type='expense' ")
            expense = c.fetchone()[0]
        except Exception as e:
            print(e)
        return expense

    def recent_transactions(self):
        try:
            c = database.table()
            c.execute('''select date,description,amount,type from transactions''')
            data = c.fetchall()
        except Exception as e:
            messagebox.showerror("error", e)
        transactions = []
        for i in data:
            transactions.append({"date": i[0], "description": i[2], "amount": i[1]})
        self.transactionframe = Recent_Transaction(master=self.scrollable_frame, width=360, corner_radius=0)
        self.transactionframe.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        for i, trans in enumerate(transactions):
            self.transactionframe.add_item(trans["date"], trans["description"], trans["amount"])

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.income.configure(fg_color=("gray75", "gray25") if name == "Manage_Income" else "transparent")
        self.expense.configure(fg_color=("gray75", "gray25") if name == "Manage_Expense" else "transparent")
        self.history.configure(fg_color=("gray75", "gray25") if name == "History" else "transparent")
        self.visualization.configure(fg_color=("gray75", "gray25") if name == "Data_Visualization" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.update_income()
            self.update_expense()
            self.recent_transactions()
        else:
            if self.home_frame is not None:
                self.home_frame.grid_forget()


        if name == "income_frame":
            self.income_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if self.income_frame is not None:
               self.income_frame.grid_forget()

        if name == "expense_frame":
            self.expense_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if self.expense_frame is not None:
                self.expense_frame.grid_forget()

        if name == "history_frame":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if self.history_frame is not None:
                self.history_frame.grid_forget()
        #
        if name == "visualization_frame":
            self.visualization_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if self.visualization_frame is not None:
                self.visualization_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def income_button_event(self):
        self.select_frame_by_name("income_frame")
        # import manageIncome
        # app=manageIncome.ManageIncome()
        # app.mainloop()

    def expense_button_event(self):
        self.select_frame_by_name("expense_frame")

    def history_click_command(self):
        self.select_frame_by_name("history_frame")

    def visualization_click_command(self):
        self.select_frame_by_name("visualization_frame")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_window_scaling(new_scaling_float)
        customtkinter.set_widget_scaling(new_scaling_float)

    def logout(self):
        self.forget()
        app=login_screen.Login()
        app.mainloop()


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
