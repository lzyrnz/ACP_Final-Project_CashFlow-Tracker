#Library
import os
import mysql.connector
from tkinter import ttk, messagebox
import customtkinter
from customtkinter import CTk, CTkImage, CTkLabel, CTkButton, CTkFrame, CTkComboBox
from PIL import Image
from loginui import current_user
import sys
import matplotlib.pyplot as plt
import subprocess

# Initialize a variable for dark mode
dark_mode_enabled = False

# Function to toggle dark mode
def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    update_theme()

# Function to update the theme based on dark mode status
def update_theme():
    global dark_mode_enabled  # Assuming dark_mode_enabled is a global variable
    theme_color = "#2A8C55" if not dark_mode_enabled else "#333333"  # Adjust color based on dark mode
    bg_color = "#B2C8BA" if not dark_mode_enabled else "#333333"  # Adjust background color based on dark mode
    summary_color ="#557C55" if not dark_mode_enabled else "#333333"

    # Update sidebar frame
    sidebar_frame.configure(fg_color=theme_color)

    # Update mainframe
    mainframe.configure(fg_color=bg_color)

    # Update summary frame
    summary_frame.configure(fg_color=summary_color)

    frame.configure(fg_color=bg_color)
      
    # Update bottom frame
    bottomframe.configure(fg_color=theme_color)

    # Update labels
    account_name_label.configure(text_color="white")

    # Update buttons
    dark_mode_button.configure(fg_color=theme_color, hover_color=theme_color)  # Update dark mode button color
    sort_button.configure(fg_color="#33b249", hover_color="#B2C8BA")
    sort2_button.configure(fg_color="#33b249", hover_color="#B2C8BA")
    show_graph_button.configure(fg_color="#33b249", hover_color="#B2C8BA")



################################################################

# Para hindi mag tuloy tuloy sa homepage
if not current_user:
    sys.exit()

################################################################

# Initialize total_income and total_expenses as global variables
total_income = 0
total_expenses = 0
total_savings = 0

################################################################

script_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(script_dir, 'img')

################################################################

# Initialize the app
app = CTk()
app.title("CashFlow Tracker")
#para asa gitna ang window
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 856
window_height = 745
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the geometry of the window
app.geometry(f"{window_width}x{window_height}+{x}+{y}")
#app.resizable(0, 0)
app.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))

################################################################

#FUNCTIONS OF EVERY ATTRIBUTES :)
# Function to create tables if they don't exist
def create_tables_if_not_exist(username):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )

    # Create a cursor
    cursor = db_connection.cursor()

    # Define the table name with the username
    table_name = f"financial_data_{username}"

    # Define SQL statements to create the user-specific table if it doesn't exist
    create_financial_data_table = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        TransactionID VARCHAR(4) PRIMARY KEY,
        Category VARCHAR(255),
        Amount DECIMAL(10, 2),
        Description TEXT,
        Date DATE
    )
    """
    cursor.execute(create_financial_data_table)

# Function to create tables if they don't exist and calculate initial totals
def create_tables_and_calculate_totals(username):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )

    # Create a cursor
    cursor = db_connection.cursor()

    # Define the user-specific table name
    table_name = f"financial_data_{username}"

    # Create the user-specific table if it doesn't exist
    create_financial_data_table = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        TransactionID VARCHAR(4) PRIMARY KEY,
        Category VARCHAR(255),
        Amount DECIMAL(10, 2),
        Description TEXT,
        Date DATE
    )
    """
    cursor.execute(create_financial_data_table)

    # Fetch data from the user-specific table
    cursor.execute(f"SELECT Amount, Category FROM {table_name}")
    transactions = cursor.fetchall()

    # Calculate initial totals
    global total_income
    global total_expenses
    global total_savings

    for amount, category in transactions:
        if category.lower() == "income":
            total_income += amount
        elif category.lower() == "expenses":
            total_expenses += amount
        elif category.lower() == "savings":
            total_savings += amount

    # Calculate total balance
    total_balance = (total_income + total_savings) - total_expenses

    # Update the summary labels
    total_balance_label.configure(text=f"Total Balance: ₱{total_balance:.2f}")
    total_income_label.configure(text=f"Total Income: ₱{total_income:.2f}")
    total_expenses_label.configure(text=f"Total Expenses: ₱{total_expenses:.2f}")
    total_savings_label.configure(text=f"Total Savings: ₱{total_savings:.2f}")

    # Close the database connection
    db_connection.close()



from tkinter import Toplevel

def on_add_transaction_click():
    # Create a new window for adding transactions
    add_transaction_window = Toplevel(app)# Center the window on the screen
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 500
    window_height = 450
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    add_transaction_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    add_transaction_window.resizable(0, 0)
    add_transaction_window.title("Add Transaction")
    add_transaction_window.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))
    add_transaction_window.configure(bg="#A6CF98")

    # Prompt for Transaction Type using CTkComboBox in the add_transaction_window
    CTkLabel(add_transaction_window, text=f"Transaction Type: ", text_color="#2A8C55", font=("Arial", 12)).pack(pady=5)
    transaction_types = ["Income", "Expenses", "Savings"]
    selected_transaction_type = CTkComboBox(master=add_transaction_window, values=transaction_types, font=("Arial", 12))
    selected_transaction_type.pack(pady=5)
  

    CTkLabel(add_transaction_window, text="Enter the Transaction ID (4 characters):", text_color="#2A8C55").pack(pady=5)
    transaction_id_entry = customtkinter.CTkEntry(add_transaction_window, placeholder_text="Transaction ID", placeholder_text_color="grey", font=("Arial", 12))
    transaction_id_entry.pack(pady=5)

    CTkLabel(add_transaction_window, text="Enter the amount:", text_color="#2A8C55").pack(pady=5)
    amount_entry = customtkinter.CTkEntry(add_transaction_window, placeholder_text="Amount", placeholder_text_color="grey", font=("Arial", 12))
    amount_entry.pack(pady=5)

    CTkLabel(add_transaction_window, text="Enter a description:", text_color="#2A8C55").pack(pady=5)
    description_entry = customtkinter.CTkEntry(add_transaction_window, placeholder_text="Description", placeholder_text_color="grey", font=("Arial", 12))
    description_entry.pack(pady=5)

    CTkLabel(add_transaction_window, text="Enter the date:", text_color="#2A8C55").pack(pady=5)
    date_entry = customtkinter.CTkEntry(add_transaction_window, placeholder_text="YYYY-MM-DD", placeholder_text_color="grey", font=("Arial", 12))
    date_entry.pack(pady=5)

    # Function to handle the "Add" button click in the add_transaction_window
    def add_button_click():
        category = selected_transaction_type.get().lower()
        transaction_id = transaction_id_entry.get()
        amount = amount_entry.get()
        description = description_entry.get()
        date = date_entry.get()

        # Perform validation and database insertion as before
        if category in ["income", "expenses", "savings"] and transaction_id and len(transaction_id) == 4 and amount and description and date:
            # Connect to the database (modify the host, user, password, and database name)
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="cashflow"
            )
            cursor = db_connection.cursor()

            # Check if the Transaction ID already exists in the user's table
            table_name = f"financial_data_{current_user}"
            cursor.execute(f"SELECT * FROM {table_name} WHERE TransactionID = %s", (transaction_id,))
            existing_record = cursor.fetchone()

            if existing_record:
                db_connection.close()
                messagebox.showerror("Duplicate Transaction ID", "Transaction ID already exists.")
            else:
                # Insert data into the user-specific table
                insert_query = f"INSERT INTO {table_name} (TransactionID, Category, Amount, Description, Date) VALUES (%s, %s, %s, %s, %s)"
                data = (transaction_id, category, amount, description, date)
                cursor.execute(insert_query, data)

                # Commit the changes and close the database connection
                db_connection.commit()
                db_connection.close()

                # Add the data to the table
                table.insert("", "end", values=(transaction_id, category, amount, description, date))
                # Update the summary after adding a transaction
                update_summary()


                # Close the add_transaction_window
                add_transaction_window.destroy()

        else:
            messagebox.showerror("Invalid Transaction Type or Missing Fields", "Please enter valid data.")

    # Create and place the "Add" button in the add_transaction_window
    CTkButton(add_transaction_window, text="Add", fg_color="#33b249", hover_color="#B2C8BA", command=add_button_click, font=("Arial Bold", 12), text_color="#ffffff").pack(pady=10)


# Add a function to delete a transaction
def delete_transaction(username):
    # Create a new window for deleting transactions
    delete_transaction_window = Toplevel(app)
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 300
    window_height = 150
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    delete_transaction_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    delete_transaction_window.resizable(0, 0)
    delete_transaction_window.title("Delete Transaction")
    delete_transaction_window.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))
    delete_transaction_window.configure(bg="#A6CF98")

    # Prompt for Transaction ID to delete
    CTkLabel(delete_transaction_window, text="Enter the Transaction ID to delete (4 characters):", text_color="#2A8C55").pack(pady=5)
    transaction_id_entry = customtkinter.CTkEntry(delete_transaction_window, placeholder_text="Transaction ID", placeholder_text_color="grey", font=("Arial", 12))
    transaction_id_entry.pack(pady=5)

    # Function to handle the "Delete" button click in the delete_transaction_window
    def delete_button_click():
        transaction_id = transaction_id_entry.get()

        if transaction_id is not None and len(transaction_id) == 4:
            # Connect to the database (modify the host, user, password, and database name)
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="cashflow"
            )

            # Create a cursor
            cursor = db_connection.cursor()

            # Check if the Transaction ID exists in the user's table
            table_name = f"financial_data_{username}"
            cursor.execute(f"SELECT * FROM {table_name} WHERE TransactionID = %s", (transaction_id,))
            existing_record = cursor.fetchone()

            if existing_record:
                # Delete the transaction with the given Transaction ID
                delete_query = f"DELETE FROM {table_name} WHERE TransactionID = %s"
                cursor.execute(delete_query, (transaction_id,))

                # Commit the changes and close the database connection
                db_connection.commit()
                db_connection.close()

                # Remove the deleted data from the table
                for item in table.get_children():
                    values = table.item(item, 'values')
                    if values[0] == transaction_id:
                        table.delete(item)
                
                # Update the summary after deleting a transaction
                update_summary()

                # Close the delete_transaction_window
                delete_transaction_window.destroy()
            else:
                db_connection.close()
                messagebox.showerror("Transaction Not Found", "Transaction with the provided ID was not found.")

        else:
            messagebox.showerror("Invalid Transaction ID", "Please enter a valid 4-character Transaction ID.")

    # Create and place the "Delete" button in the delete_transaction_window
    CTkButton(delete_transaction_window, text="Delete", fg_color="#b23333", hover_color="#BA9C9C", command=delete_button_click, font=("Arial Bold", 12), text_color="#ffffff").pack(pady=10)


def modify_transaction(username):
    # Create a new window for modifying transactions
    modify_transaction_window = Toplevel(app)
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 400
    window_height = 300
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    modify_transaction_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    modify_transaction_window.resizable(0, 0)
    modify_transaction_window.title("Modify Transaction")
    modify_transaction_window.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))
    modify_transaction_window.configure(bg="#A6CF98")

    # Prompt for Transaction ID to modify
    CTkLabel(modify_transaction_window, text="Enter the Transaction ID to modify (4 characters):", text_color="#2A8C55").pack(pady=5)
    transaction_id_entry = customtkinter.CTkEntry(modify_transaction_window, placeholder_text="Transaction ID", placeholder_text_color="grey", font=("Arial", 12))
    transaction_id_entry.pack(pady=5)

    # Prompt for what to modify (Amount, Description, or Date)
    CTkLabel(modify_transaction_window, text="What would you like to modify:", text_color="#2A8C55").pack(pady=5)
    modification_choices = ["Amount", "Description", "Date"]
    modification_choice_combobox = CTkComboBox(master=modify_transaction_window, values=modification_choices, font=("Arial", 12))
    modification_choice_combobox.pack(pady=5)

    # Prompt for the new value
    CTkLabel(modify_transaction_window, text="Enter the new value:", text_color="#2A8C55").pack(pady=5)
    new_value_entry = customtkinter.CTkEntry(modify_transaction_window, placeholder_text="New Value", placeholder_text_color="grey", font=("Arial", 12))
    new_value_entry.pack(pady=5)

    # Function to handle the "Modify" button click in the modify_transaction_window
    def modify_button_click():
        transaction_id = transaction_id_entry.get()
        modification_choice = modification_choice_combobox.get().lower()
        new_value = new_value_entry.get()

        if transaction_id is not None and len(transaction_id) == 4:
            # Connect to the database (modify the host, user, password, and database name)
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="cashflow"
            )

            # Create a cursor
            cursor = db_connection.cursor()

            # Check if the Transaction ID exists in the user's table
            table_name = f"financial_data_{username}"
            cursor.execute(f"SELECT * FROM {table_name} WHERE TransactionID = %s", (transaction_id,))
            existing_record = cursor.fetchone()

            if existing_record:
                if modification_choice in ["amount", "description", "date"]:
                    # Update the specified field with the new value
                    update_query = f"UPDATE {table_name} SET {modification_choice} = %s WHERE TransactionID = %s"
                    cursor.execute(update_query, (new_value, transaction_id))

                    # Commit the changes and close the database connection
                    db_connection.commit()
                    db_connection.close()

                    # Re-load transactions and populate the table
                    load_transactions(username)  # Pass the username to the load_transactions function
                    # Update the summary after deleting a transaction
                    update_summary()

                    # Close the modify_transaction_window
                    modify_transaction_window.destroy()
                else:
                    db_connection.close()
                    messagebox.showerror("Invalid Modification Choice", "Please select a valid modification choice.")
            else:
                db_connection.close()
                messagebox.showerror("Transaction Not Found", "Transaction with the provided ID was not found.")
        else:
            messagebox.showerror("Invalid Transaction ID", "Please enter a valid 4-character Transaction ID.")

    # Create and place the "Modify" button in the modify_transaction_window
    CTkButton(modify_transaction_window, text="Modify", fg_color="#3380b2", hover_color="#9CBABA", command=modify_button_click, font=("Arial Bold", 12), text_color="#ffffff").pack(pady=10)

def search_transaction():
    transaction_id = search_entry.get()
    if len(transaction_id) == 4:
        for item in table.get_children():
            values = table.item(item, 'values')
            if values[0] == transaction_id:
                table.selection_set(item)  # Highlight the found row
                table.see(item)  # Ensure that the found row is visible in the table
                break
        else:
            messagebox.showinfo("Transaction Not Found", "Transaction with the provided ID was not found.")
    else:
        messagebox.showinfo("Invalid Transaction ID", "Please enter a 4-character Transaction ID.")

# Function to load saved transactions from the database and populate the table
def load_transactions(username):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )

    # Create a cursor
    cursor = db_connection.cursor()

    # Define the user-specific table name
    table_name = f"financial_data_{username}"

    # Fetch data from the user-specific table
    cursor.execute(f"SELECT TransactionID, Category, Amount, Description, Date FROM {table_name}")
    transactions = cursor.fetchall()

    # Clear the table before populating it to avoid duplicates
    for row in table.get_children():
        table.delete(row)

    # Populate the table with fetched data
    for transaction in transactions:
        table.insert("", "end", values=transaction)

    # Close the database connection
    db_connection.close()

# Function to log out the user and return to the login UI
def logout():
    # Ask the user for confirmation
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to log out?")

    if confirmed:
        app.destroy()  # Close the current window (main window of main.py)

        # Start a new instance of the Python interpreter with loginui.py
        subprocess.run(["python", os.path.join(script_dir, "main.py")])


def filter_transactions_by_category(username, category):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )

    # Create a cursor
    cursor = db_connection.cursor()

    # Define the user-specific table name
    table_name = f"financial_data_{username}"

    # Fetch data from the user-specific table for the selected category
    cursor.execute(f"SELECT TransactionID, Category, Amount, Description, Date FROM {table_name} WHERE Category = %s", (category,))
    transactions = cursor.fetchall()

    # Clear the table before populating it to avoid duplicates
    for row in table.get_children():
        table.delete(row)

    # Populate the table with fetched data
    for transaction in transactions:
        table.insert("", "end", values=transaction)

    # Close the database connection
    db_connection.close()


def sort_by_category(column):
    if column == "Amount":
        selected_option = sort_options.get()
        if selected_option != "Default":
            sort_amount()
    else:
        selected = selected_category.get()
        if selected == "Show All":
            load_transactions(current_user)
        else:
            filter_transactions_by_category(current_user, selected)

def sort_amount():
    selected_option = sort_options.get()
    if selected_option == "Sort to smallest to largest amount":
        table_sort_by_amount("Amount", reverse=False)
    elif selected_option == "Sort to largest to smallest amount":
        table_sort_by_amount("Amount", reverse=True)
    elif selected_option == "Latest Date":
        table_sort_by_date(reverse=True)
    elif selected_option == "Oldest Date":
        table_sort_by_date(reverse=False)
    else:
        load_transactions(current_user)  # Reset to the default order

def table_sort_by_amount(column, reverse=False):
    # Function to sort the table by the "Amount" column
    items = table.get_children()
    items = [(table.item(item, 'values'), item) for item in items]
    items.sort(key=lambda x: float(x[0][2]), reverse=reverse)

    for i, (values, item) in enumerate(items):
        table.move(item, '', i)

# Function to sort the table by the "Date" column
def table_sort_by_date(reverse=False):
    items = table.get_children()
    items = [(table.item(item, 'values'), item) for item in items]
    items.sort(key=lambda x: x[0][4], reverse=reverse)  # Index 4 corresponds to the "Date" column

    for i, (values, item) in enumerate(items):
        table.move(item, '', i)


def search_transaction():
    transaction_id = search_entry.get()
    if len(transaction_id) == 4:
        for item in table.get_children():
            values = table.item(item, 'values')
            if values[0] == transaction_id:
                table.selection_set(item)  # Highlight the found row
                table.see(item)  # Ensure that the found row is visible in the table
                break
        else:
            # You can update the summary labels or show a message here
            messagebox.showinfo("Transaction Not Found", "Transaction with the provided ID was not found.")
    else:
        # You can update the summary labels or show a message here
        messagebox.showinfo("Invalid Transaction ID", "Please enter a 4-character Transaction ID.")

# Function to update summary information
def update_summary():
    global total_income
    global total_expenses
    global total_savings

    # Calculate total balance, income, expenses, and savings
    total_balance = 0
    total_income = 0
    total_expenses = 0
    total_savings = 0

    for item in table.get_children():
        values = table.item(item, 'values')
        amount = float(values[2])
        if values[1].lower() == "income":
            total_income += amount
        elif values[1].lower() == "expenses":
            total_expenses += amount
        elif values[1].lower() == "savings":
            total_savings += amount

    total_balance = (total_income + total_savings) - total_expenses

    # Update the summary labels
    total_balance_label.configure(text=f"Total Balance: ₱{total_balance:.2f}")
    total_income_label.configure(text=f"Total Income: ₱{total_income:.2f}")
    total_expenses_label.configure(text=f"Total Expenses: ₱{total_expenses:.2f}")
    total_savings_label.configure(text=f"Total Savings: ₱{total_savings:.2f}")

# Create a function to refresh the summary and filter
def refresh_summary_and_filter():
    load_transactions(current_user)
    update_summary()


# Create a bar chart for income, expenses, and savings
def plot_graph(graph_type):
    # Ensure that total_income, total_expenses, and total_savings are accessible
    global total_income
    global total_expenses
    global total_savings

    income = total_income
    expenses = total_expenses
    savings = total_savings

    categories = ['Income', 'Expenses', 'Savings']
    values = [income, expenses, savings]

    plt.figure(figsize=(6, 4))

    if graph_type == "Bar Graph":
        plt.bar(categories, values, color=['green', 'red', 'blue'])
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.title('Income, Expenses, and Savings (Bar Graph)')
    elif graph_type == "Line Graph":
        # Plot connecting line with black color
        plt.plot(categories, values, color='black', linestyle='-', linewidth=2, zorder=1)

        # Plot markers with specified colors on top of the line
        marker_colors = ['green', 'red', 'blue']
        for category, value, marker_color in zip(categories, values, marker_colors):
            plt.scatter(category, value, color=marker_color, marker='o', s=100, zorder=2)

        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.title('Income, Expenses, and Savings (Line Graph)')

    plt.grid(True)
    plt.show()
    

################################################################

################################################################

# Create the sidebar
sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=176, height=650, border_width=5, border_color="black", corner_radius=50) 
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

# Replace the CTkLabel with a CTkButton for the logo
logo_img_data = Image.open(os.path.join(img_folder, 'logo.png'))
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(107.98, 105.82))
dark_mode_button = CTkButton(master=sidebar_frame, image=logo_img, command=toggle_dark_mode,text="", fg_color="#2A8C55", hover_color="#2A8C55")
dark_mode_button.pack(pady=(38, 0), anchor="center")

package_img_data = Image.open(os.path.join(img_folder, 'user_icon.png'))
package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)



add_transaction_button = CTkButton(master=sidebar_frame, image=package_img, text="Add Transaction", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#207244", anchor="w", command=on_add_transaction_click)
add_transaction_button.pack(anchor="center", ipady=5, pady=(60, 0))

# Add a "Delete Transaction" button
delete_img_data = Image.open(os.path.join(img_folder, "delete.png"))
delete_img = CTkImage(dark_image=delete_img_data, light_image=delete_img_data)

delete_transaction_button = CTkButton(master=sidebar_frame, image=delete_img, text="Delete Transaction", fg_color="#fff", font=("Arial Bold", 12.75 ), text_color="#2A8C55", hover_color="#207244", anchor="w", command=lambda: delete_transaction(current_user))
delete_transaction_button.pack(anchor="center", ipady=5, pady=(16, 0))

# Add a "Modify Transaction" button
modify_img_data = Image.open(os.path.join(img_folder, "modify.png"))
modify_img = CTkImage(dark_image=modify_img_data, light_image=modify_img_data)

modify_transaction_button = CTkButton(master=sidebar_frame, image=modify_img, text="Modify Transaction", fg_color="#fff", font=("Arial Bold", 13), text_color="#2A8C55", hover_color="#207244", anchor="w", command=lambda: modify_transaction(current_user))
modify_transaction_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Display the account name
account_name_label = CTkLabel(master=sidebar_frame, text=f"Account: {current_user}", text_color="white", font=("Arial Bold", 14))
account_name_label.pack(pady=(100, 0), anchor="center")

# Add a "Logout" button in the sidebar
logout_img_data = Image.open(os.path.join(img_folder, "logout.png"))
logout_img = CTkImage(dark_image=logout_img_data, light_image=logout_img_data)

logout_button = CTkButton(master=sidebar_frame, image=logout_img, text="   Logout", fg_color="#fff", font=("Arial Bold", 12.75), text_color="#2A8C55", hover_color="#207244", anchor="w", command=logout)
logout_button.pack(anchor="center", ipady=5, pady=(10, 0))

################################################################

# Create a frame for the table
mainframe = CTkFrame(app, width=800, height=645, fg_color="#B2C8BA", border_width=0.5, border_color="black", corner_radius=25)
mainframe.pack(fill="both", expand=True, padx=10, pady=10)

# Create a frame to hold the table
frame = CTkFrame(mainframe, width=720, height=645, fg_color="#B2C8BA")
frame.pack(padx=20, pady=20)

# Create a treeview widget to display the information
table = ttk.Treeview(frame, columns=("TransactionID", "Category", "Amount", "Description", "Date"), show="headings")

# Style the treeview widget
style = ttk.Style()
style.configure("Treeview", font=('Helvetica', 12), rowheight=25, background="#F2FFE9", fieldbackground="#FFFFFF")
style.configure("Treeview.Heading", font=('Helvetica', 10,'bold'), background="#A6CF98", foreground="black")

table.column("TransactionID", width=150, anchor="center")
table.column("Category", width=95, anchor="center")
table.column("Amount", width=100, anchor="center")
table.column("Description", width=140, anchor="center")
table.column("Date", width=120, anchor="center")

# Set up the headings for your table
table.heading("TransactionID", text="Transaction ID", command=lambda: sort_by_category("TransactionID"))
table.heading("Category", text="Category", command=lambda: sort_by_category("Category"))
table.heading("Amount", text="Amount", command=lambda: sort_by_category("Amount"))
table.heading("Description", text="Description", command=lambda: sort_by_category("Description"))
table.heading("Date", text="Date", command=lambda: sort_by_category("Date"))

table.pack(fill="both", expand=True, padx=10, pady=10)

################################################################

# Create a frame for the summary
summary_frame = CTkFrame(app, width=620, height=350, fg_color="#A6CF98", corner_radius=30)
summary_frame.pack(padx=20, pady=(10, 0), fill="x", anchor="w")

# Create labels to display the summary information
total_balance_label = CTkLabel(master=summary_frame, text="Total Balance: ₱0.00", font=("Arial Bold", 12), text_color="#fff")
total_balance_label.grid(row=0, column=0, padx=(40, 130), pady=10)

total_income_label = CTkLabel(master=summary_frame, text="Total Income: ₱0.00", font=("Arial Bold", 12), text_color="#fff")
total_income_label.grid(row=0, column=1, padx=(30, 10), pady=10)

total_expenses_label = CTkLabel(master=summary_frame, text="Total Expenses: ₱0.00", font=("Arial Bold", 12), text_color="#fff")
total_expenses_label.grid(row=1, column=0, padx=(50, 130), pady=10)

# Define the total_savings_label and set its initial text
total_savings_label = CTkLabel(master=summary_frame, text="Total Savings: ₱0.00", font=("Arial Bold", 12), text_color="#fff")
total_savings_label.grid(row=1, column=1, padx=(20, 10), pady=10)

################################################################

bottomframe = CTkFrame(app, width=640, height=300, fg_color="#86A789", border_width=15, border_color="black", corner_radius=30)
bottomframe.pack(fill="both", expand=True)

# Create the category selection ComboBox
selected_category = CTkComboBox(master=bottomframe, values=["Show All", "Income", "Expenses", "Savings"])
selected_category.set("Show All")  # Set the initial selection to "Show All"
selected_category.grid(row=0, column=0, padx=20, pady=40, sticky="w")

# Create a "Sort" button
sort_button = CTkButton(master=bottomframe, text="Filter", fg_color="#33b249", hover_color="#B2C8BA", command=lambda: sort_by_category(None), font=("Arial Bold", 12), text_color="#ffffff")
sort_button.grid(row=0, column=1, padx=(1, 0), pady=20, sticky="w")

# Create the sorting options ComboBox
sort_options = CTkComboBox(master=bottomframe, values=["Sort to smallest to largest amount", "Sort to largest to smallest amount", "Latest Date", "Oldest Date", "Default"])
sort_options.set("Default")  # Set the initial selection to "Default"
sort_options.grid(row=0, column=2, padx=20, pady=20, sticky="w")

# Create a "Sort" button for sorting by amount
sort2_button = CTkButton(master=bottomframe, text="Sort", fg_color="#33b249", hover_color="#B2C8BA", command=sort_amount, font=("Arial Bold", 12), text_color="#ffffff")
sort2_button.grid(row=0, column=3, padx=(0, 10), pady=20, sticky="w")

# Create the search Entry using CTkEntry
search_entry = customtkinter.CTkEntry(master=bottomframe, placeholder_text="Search Transaction ID", placeholder_text_color="white", font=("Arial", 12))
search_entry.grid(row=1, column=0, padx=20, pady=20, sticky="w")

# Create a "Search" button using CTkButton
search_button = CTkButton(master=bottomframe, text="Search", fg_color="#33b249", hover_color="#B2C8BA", command=search_transaction, font=("Arial Bold", 12), text_color="#ffffff")
search_button.grid(row=1, column=1, padx=(1, 0), pady=20, sticky="w")

# Create the graph type selection ComboBox
graph_type_combobox = CTkComboBox(master=bottomframe, values=["Bar Graph", "Line Graph"])
graph_type_combobox.set("Bar Graph")
graph_type_combobox.grid(row=1, column=2, padx=20, pady=20, sticky="w")

# Create a button to display the selected graph type
show_graph_button = CTkButton(master=bottomframe, text="Show Graph", fg_color="#33b249", hover_color="#B2C8BA", command=lambda: plot_graph(graph_type_combobox.get()), font=("Arial Bold", 12), text_color="#ffffff")
show_graph_button.grid(row=1, column=3, padx=(1, 0), pady=20, sticky="w")


################################################################

# Load saved transactions and create tables when the application starts
create_tables_if_not_exist(current_user)
load_transactions(current_user)
update_theme()


# After user login
if current_user:
    create_tables_and_calculate_totals(current_user)
    load_transactions(current_user)
    update_summary()


app.mainloop()