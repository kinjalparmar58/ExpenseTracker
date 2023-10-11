from tkinter import messagebox
import customtkinter
import database
import tkinter as tk

cur = database.c


def get_month_names():
    cur.execute("SELECT DISTINCT strftime('%m-%Y', date) FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()
    return [row[0] for row in rows]


def show_transactions():
    selected_month = month_variable

    if not selected_month:
        tk.messagebox.showerror("Error", "Please select a month")
        return

    # Fetch all transactions for the selected month from the database

    scrollable_frame = customtkinter.CTkScrollableFrame(root, label_text="Recent Transactions", width=360)
    scrollable_frame.pack(side="top")
    scrollable_frame.grid_columnconfigure(0,)
    try:
        cur.execute("SELECT id,date,description,amount,type FROM transactions WHERE strftime('%m-%Y', date)=?",
                    (selected_month,))
        rows = cur.fetchall()
    except Exception as e:
        messagebox.showerror("error", e)
    transactions = []
    for i in rows :
        transactions.append({"id": i[0], "date": i[1], "description": i[2], "amount": i[3], "type": i[4]})
    transactionframe = Recent_Transaction(master=scrollable_frame, width=360, corner_radius=0)
    transactionframe.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
    for i, trans in enumerate(transactions):
        transactionframe.add_item(trans["id"], trans["date"], trans["description"], trans["amount"], trans["type"])


def trancHistory(Root):
    global month_variable, root
    transaction_frame = customtkinter.CTkFrame(Root, corner_radius=0, fg_color="transparent")
    root = transaction_frame

    month_menu = customtkinter.CTkComboBox(root, values=get_month_names())
    month_menu.pack(side="top")
    month_variable = month_menu.get()

    show_button = customtkinter.CTkButton(root, text="Show Transactions", command=show_transactions)
    show_button.pack(side="top")

    return root


class Recent_Transaction(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.date_label = []
        self.disc_label = []
        self.amount_label = []
        self.type_label = []
        self.id_label = []

    def add_item(self, id, date, amount, disc, type):

        label1 = customtkinter.CTkLabel(self, text=date, compound="left", padx=5, anchor="w")
        label2 = customtkinter.CTkLabel(self, text=disc,  compound="left", padx=5, anchor="w")
        label3 = customtkinter.CTkLabel(self, text=amount, compound="left", padx=5, anchor="w")
        label4 = customtkinter.CTkLabel(self, text=type, compound="left", padx=5, anchor="w")
        label5 = customtkinter.CTkLabel(self, text=id , compound="left", padx=5, anchor="w")

        label5.grid(row=len(self.id_label), column=0, pady=(0, 10),)
        label1.grid(row=len(self.date_label), column=1, pady=(0, 10),)
        label2.grid(row=len(self.disc_label), column=2, pady=(0, 10), padx=5)
        label3.grid(row=len(self.amount_label), column=3, pady=(0, 10), padx=5)
        label4.grid(row=len(self.amount_label), column=4, pady=(0, 10), padx=5)

        if type == "income":
            label1.configure(text_color='green')
            label2.configure(text_color='green')
            label3.configure(text_color='green')
            label4.configure(text_color='green')
            label5.configure(text_color='green')

        else:
            label1.configure(text_color='red')
            label2.configure(text_color='red')
            label3.configure(text_color='red')
            label4.configure(text_color='red')
            label5.configure(text_color='red')

        self.date_label.append(label1)
        self.disc_label.append(label2)
        self.amount_label.append(label3)
        self.type_label.append(label4)
        self.id_label.append(label5)
