import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
import database



def IncomeExpensePieChart(Root):
    global root
    chart_frame = customtkinter.CTkFrame(Root, corner_radius=0, fg_color="transparent")
    root = chart_frame
    chart_frame.columnconfigure(2)

    income_button = customtkinter.CTkButton(root, text="Income Chart", command=create_income)
    income_button.grid(column=0 ,row=0, columnspan=2,padx=(30,20),pady=(0,10))

    expense_button = customtkinter.CTkButton(root, text="Expense Chart", command=create_expense_chart)
    expense_button.grid(column=2, row=0, columnspan=2,padx=(30,20),pady=(0,10))

    basic_chart()
    return root
#
AllTransactions = []

def get_all_transactions():
    data = database.get_transactions()
    for i in data:
        AllTransactions.append(i)
    return AllTransactions

def create_income():
    pass

def create_expense_chart():
    pass

def basic_chart():
    c = database.c
    c.execute("SELECT type, SUM(amount) FROM Transactions GROUP BY type")
    data = c.fetchall()

    # plt.style.use('background')
    fig = plt.Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)
    fig.set_animated(True)

    ax.pie([x[1] for x in data], labels=[x[0] for x in data], autopct='%1.1f%%')

    canvas = FigureCanvasTkAgg(fig, master=root,resize_callback=3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, columnspan=4 , pady=40, sticky="nw")

def get_percentage(part, whole):
    percentage = 100 * float(part) / float(whole)
    return percentage / 100