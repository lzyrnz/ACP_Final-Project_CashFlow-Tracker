import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from customtkinter import CTkButton, CTkLabel
import customtkinter
import os
import subprocess

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()

# Center the window on the screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 600
window_height = 460
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

app.title("Admin Panel")
app.resizable(0, 0)

# Dynamically determine the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(script_dir, 'img')

app.wm_iconbitmap(os.path.join(img_folder, "cash.ico"))

# Connect to the 'cashflow' database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cashflow"
)

show_password_visible = False  # Initialize password visibility state

def close_application():
    app.destroy()
    subprocess.run(["python", os.path.join(script_dir, "main.py")])

def delete_user():
    # Get the selected user from the table
    selected_user = users_table.item(users_table.selection())['values']

    if selected_user:
        username = selected_user[0]
        if username == 'admin':
            messagebox.showerror("Error", "Cannot delete the admin user.")
        else:
            cursor = conn.cursor()
            delete_query = "DELETE FROM users WHERE username = %s"
            cursor.execute(delete_query, (username,))
            conn.commit()
            cursor.close()
            load_users()

def show_password():
    global show_password_visible
    selected_item = users_table.selection()
    for item in selected_item:
        selected_user = users_table.item(item)
        if selected_user:
            username = selected_user['values'][0]
            password = actual_passwords.get(username, '')

            if show_password_visible:
                # Password is visible, mask it
                masked_password = '*' * len(password)
                users_table.item(item, values=(username, masked_password))
            else:
                # Password is masked, show the actual password
                unmasked_password = password
                users_table.item(item, values=(username, unmasked_password))

    show_password_visible = not show_password_visible  # Toggle visibility state

def load_users():
    global actual_passwords
    actual_passwords = {}  # Store actual passwords

    # Clear the table
    for record in users_table.get_children():
        users_table.delete(record)

    # Fetch users from the database
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    cursor.close()

    # Populate the table with users and asterisks for passwords
    for user in users:
        username, password = user[0], user[1]
        actual_passwords[username] = password  # Store the actual password
        masked_password = '*' * len(password)
        users_table.insert("", "end", values=(username, masked_password))

# Create a label to display the welcome message
welcome_label = CTkLabel(app, text="Welcome, Admin!", font=("Arial Bold", 30))
welcome_label.pack(pady=10)

# Create a table to display users and passwords
users_table = ttk.Treeview(app, columns=("Username", "Password"), show="headings")
users_table.heading("Username", text="Username")
users_table.heading("Password", text="Password")
users_table.pack(pady=(20, 0))

load_users()

# Create a "Delete User" button
delete_user_button = CTkButton(app, text="Delete User", fg_color="#ff3333", hover_color="#B2C8BA", command=delete_user)
delete_user_button.pack(pady=10)

# Create a "Show/Hide Password" button
show_password_button = CTkButton(app, text="Show/Hide Password", fg_color="#33b249", hover_color="#B2C8BA", command=show_password)
show_password_button.pack(pady=10)

# Create a "Close" button
close_button = CTkButton(app, text="Close", fg_color="#3333ff", hover_color="#B2C8BA", command=close_application)
close_button.pack(pady=10)

app.mainloop()
