from tkinter import *
import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Function to handle sign-up
def sign_up_clicked():
    username = entry1.get()
    email = entry2.get()
    password = entry3.get()
    confirm_password = entry4.get()

    if password != confirm_password:
        print("Passwords do not match")
    else:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        print("User signed up successfully")

# Function to handle login
def login_clicked():
    username = entry1.get()
    password = entry3.get()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        print("Login successful")
        # Redirect to your main application window or perform any other action
    else:
        print("Invalid username or password")

# Create the main application window
app = customtkinter.CTk()
app.geometry("800x600")
app.title('FaceFury Login')

# UI components
img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()

frame = customtkinter.CTkFrame(master=l1, width=600, height=320, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Sign Up to FaceFury 😎", font=('Century Gothic', 20))
l2.place(x=50, y=45)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Email")
entry2.place(x=325, y=110)

entry3 = customtkinter.CTkEntry(master=frame, show="*", width=220, placeholder_text="Password")
entry3.place(x=50, y=160)

entry4 = customtkinter.CTkEntry(master=frame, show="*", width=220, placeholder_text="Confirm Password")
entry4.place(x=325, y=160)

button1 = customtkinter.CTkButton(master=frame, width=220, text='Sign up', corner_radius=6, command=sign_up_clicked)
button1.place(x=325, y=210)

l3 = customtkinter.CTkLabel(master=frame, text="Already have an account?", font=('Century Gothic', 12))
l3.place(x=50, y=210)

button2 = customtkinter.CTkButton(master=frame, width=6, text='Login', command=login_clicked, fg_color='transparent')
button2.place(x=208, y=211)

app.resizable(False, False)
app.mainloop()
