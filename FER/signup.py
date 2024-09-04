from tkinter import *
import tkinter
import customtkinter
from PIL import ImageTk, Image
import sqlite3
import login
from tkinter import messagebox
import signup
import re

customtkinter.set_appearance_mode("system") #can set light or dark mode
customtkinter.set_default_color_theme("blue")

def main():
    app = customtkinter.CTk() #creating custom tkinter window
    app.geometry("800x600")
    app.title('FaceFury Signup')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
                   
                   CREATE TABLE IF NOT EXISTS users(
                       username TEXT NOT NULL,
                       email TEXT NOT NULL,
                       password TEXT NOT NULL
                    )               
                   ''')

    conn.commit()

    def login_clicked():
        print("Login Clicked")
        app.destroy()
        # Open the login window
        login.main()
        
    # def toggle_password_visibility():
    #     # Toggle password visibility
    #     if entry3.cget('show') == '':
    #         entry3.config(show='*')
    #         show_password_button.config(text='Show')
    #     else:
    #         entry3.config(show='')
    #         show_password_button.config(text='Hide')

    def button_function():
        username = entry1.get()
        email = entry2.get()
        password = entry3.get()
        confirm_password = entry4.get()

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

        # Check if email matches regex pattern
        if not re.match(email_pattern, email):
            messagebox.showinfo("Error", "Invalid email format")
            return

        # Check if password matches regex pattern
        if not re.match(password_pattern, password):
            messagebox.showinfo("Error", "Password must be at least 8 characters long and contain at least one letter and one number")
            return

        # Check if password and confirm password match
        if password != confirm_password:
            messagebox.showinfo("Error","Passwords do not match")
            return

        # Query the database to check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showinfo("Error", "Username already exists")
            return

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        messagebox.showinfo("Success", "User signed up successfully")
        
        # Navigate back to login page
        app.destroy()  # Close the signup window
        login.main()   # Open the login window


      
    # img1=ImageTk.PhotoImage(Image.open("pattern.png"))
    img1 = ImageTk.PhotoImage(Image.open(r"C:\Users\ROG\Desktop\HCK\FYP\code2\pattern.png"))

    l1 = customtkinter.CTkLabel(master=app, image = img1)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=600, height=320, corner_radius = 15)
    frame.place(relx=0.5,rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Sign Up to FaceFury 😎", font=('Century Gothic', 20))
    l2.place(x=50, y=45)

    entry1=customtkinter.CTkEntry(master=frame, width=220,placeholder_text="Username")
    entry1.place(x=50,y=110)

    entry2=customtkinter.CTkEntry(master=frame, width=220,placeholder_text="Email")
    entry2.place(x=325,y=110)

    entry3=customtkinter.CTkEntry(master=frame,show="*", width=220,placeholder_text="Password")
    entry3.place(x=50,y=160)

    entry4=customtkinter.CTkEntry(master=frame,show="*", width=220,placeholder_text="Confirm Password")
    entry4.place(x=325,y=160)
    
    # show_password_button = customtkinter.CTkButton(master=frame, width=6, text='Show', command=toggle_password_visibility)
    # show_password_button.place(x=515, y=160)
    
    

    button1 = customtkinter.CTkButton(master=frame, width=220, text='Sign up',corner_radius=6, command=button_function)
    button1.place(x=325, y=210)

    l3 = customtkinter.CTkLabel(master=frame, text="Already have an account?", font=('Century Gothic', 12))
    l3.place(x=50, y=210)

    button2 = customtkinter.CTkButton(master=frame, width=6, text='Login', command=login_clicked, fg_color='transparent',)
    button2.place(x=208, y=211)

    app.resizable(False,False)
    app.mainloop()

if __name__ == "__main__":
    main()
