import customtkinter
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
import mysql.connector
import subprocess
import os

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
app.title("CashFlow Tracker - Sign Up")

# Dynamically determine the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(script_dir, 'img')
app.wm_iconbitmap(os.path.join(script_dir, 'img', 'cash.ico'))

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cashflow"
)

# Define the email and password icons as CTkImage objects
user_icon_data = CTkImage(
    dark_image=Image.open(os.path.join(img_folder, 'user_icon.png')),
    light_image=Image.open(os.path.join(img_folder, 'user_icon.png')),
    size=(20, 20)
)
password_icon_data = CTkImage(
    dark_image=Image.open(os.path.join(img_folder, 'password-icon.png')),
    light_image=Image.open(os.path.join(img_folder, 'password-icon.png')),
    size=(17, 17)
)

# Function to switch back to the login page
def switch_to_login_page():
    app.destroy()
    subprocess.run(["python", os.path.join(script_dir, "main.py")])

def checkinfo():
    # Check if username and password are complete
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        cursor = conn.cursor()
        # Check if the username already exists in the database
        check_query = "SELECT * FROM users WHERE username = %s"
        check_values = (username,)
        cursor.execute(check_query, check_values)
        existing_user = cursor.fetchone()

        if existing_user:
            # If the username is already in the database, show an error
            messagebox.showerror("Username Taken", "This username is already taken.")
        else:
            # If the username is not in the database, proceed with registration
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            insert_values = (username, password)
            cursor.execute(insert_query, insert_values)
            conn.commit()
            cursor.close()

            # Provide feedback to the user that registration was successful
            success_label = customtkinter.CTkLabel(master=frame, text="Sign up successful!", font=("Roboto", 12))
            success_label.pack(pady=12, padx=10)

            # Show a message box to inform the user that registration was successful
            messagebox.showinfo("Registration Successful", "Account successfully registered.")

            # Close the registration window
            app.destroy()

            subprocess.run(["python", os.path.join(script_dir, "main.py")])
    else:
        messagebox.showerror("Incomplete Fields", "Username and password must be complete.")

side_img_data = Image.open(os.path.join(img_folder, 'side-img.png'))

side_img = customtkinter.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))

customtkinter.CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = customtkinter.CTkFrame(master=app, width=300, height=480, fg_color="#1a1a1a")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

customtkinter.CTkLabel(master=frame, text="Signup with Cashflow", text_color="white", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
customtkinter.CTkLabel(master=frame, text="Sign up for an account", text_color="white", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

customtkinter.CTkLabel(master=frame, text="  Username:", text_color="white", anchor="w", justify="left", font=("Arial Bold", 14), image=user_icon_data, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
username_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#333333", border_color="grey", border_width=1, text_color="white")
username_entry.pack(anchor="w", padx=(25, 0))

customtkinter.CTkLabel(master=frame, text="  Password:", text_color="white", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon_data, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#333333", border_color="grey", border_width=1, text_color="white", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

signup_button = customtkinter.CTkButton(master=frame, text="Sign Up", fg_color="#232D3F", hover_color="#61677A", command=checkinfo, font=("Arial Bold", 12), text_color="#ffffff", width=225)
signup_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))

# Create a button to switch back to the login page
login_button = customtkinter.CTkButton(master=frame, text="Back to Login", fg_color="#2C3333", hover_color="#454545", command=switch_to_login_page, font=("Arial Bold", 12), text_color="#ffffff", width=225)
login_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))
customtkinter.CTkLabel(master=frame, text="Already have an account?", text_color="#7E7E7E", anchor="w", justify="right", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

app.mainloop()
