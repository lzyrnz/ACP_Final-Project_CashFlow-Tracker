import customtkinter
from tkinter import messagebox
from PIL import Image
from tkinter import messagebox
import mysql.connector
from mysql.connector import errors as mysql_errors
import os

current_user = None

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()

# Center the window on the screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 600
window_height = 480
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
app.resizable(0, 0)
app.title("CashFlow Tracker")

# Dynamically determine the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(script_dir, 'img')
app.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))

# Attempt to connect to the 'cashflow' database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )
except mysql_errors.DatabaseError:
    # If the database doesn't exist, create it
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    create_database_query = "CREATE DATABASE IF NOT EXISTS cashflow"
    cursor.execute(create_database_query)
    cursor.close()

    # Now, reconnect to the newly created database 'cashflow'
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cashflow"
    )

# Create a table for users in 'cashflow_registration' if it doesn't exist
cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(20),
    balance DECIMAL(10, 2) DEFAULT 0.0  -- Add the 'balance' column
)
"""
cursor.execute(create_table_query)
conn.commit()
cursor.close()

# Function to switch to the signup page
def switch_to_signup_page():
    app.destroy()
    import signupui

def switch_to_homepageui():
    global current_user
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        if username == "admin" and password == "cashflow1":
            app.destroy()
            import admin
        else:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()

            if user:
                current_user = username
                app.destroy()
            else:
                messagebox.showerror("Incorrect Credentials", "Incorrect username or password.")
    else:
        messagebox.showerror("Incomplete Fields", "Username and password must be complete.")

# Load images using dynamically determined paths
side_img_data = Image.open(os.path.join(img_folder, 'side-img.png'))
user_icon_data = Image.open(os.path.join(img_folder, 'user_icon.png'))
password_icon_data = Image.open(os.path.join(img_folder, 'password-icon.png'))

side_img = customtkinter.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = customtkinter.CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20, 20))
password_icon = customtkinter.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

customtkinter.CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = customtkinter.CTkFrame(master=app, width=300, height=480, fg_color="#D2E3C8")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

customtkinter.CTkLabel(master=frame, text="CashFlow Tracker!", text_color="#86A789", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
customtkinter.CTkLabel(master=frame, text="Log in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

customtkinter.CTkLabel(master=frame, text="  Username:", text_color="#86A789", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
username_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#B2C8BA", border_color="#86A789", border_width=1, text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

customtkinter.CTkLabel(master=frame, text="  Password:", text_color="#86A789", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#B2C8BA", border_color="#86A789", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

login_button = customtkinter.CTkButton(master=frame, text="Login", fg_color="#33b249", hover_color="#B2C8BA", command=switch_to_homepageui, font=("Arial Bold", 12), text_color="#ffffff", width=225)
login_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))

# Create a button to switch to the signup page
signup_button = customtkinter.CTkButton(master=frame, text="Sign up", fg_color="#86A789", hover_color="#B2C8BA", command=switch_to_signup_page, font=("Arial Bold", 12), text_color="#ffffff", width=225)
signup_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))

customtkinter.CTkLabel(master=frame, text="Don't have an account?", text_color="#7E7E7E", anchor="w", justify="right", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

app.mainloop()