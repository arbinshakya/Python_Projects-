from tkinter import *
import tkinter
import customtkinter
from PIL import ImageTk, Image
import subprocess
import os
import sqlite3
from tkinter import messagebox
import signup
import threading

print(os.getcwd())

customtkinter.set_appearance_mode("system")  # Can set light or dark mode
customtkinter.set_default_color_theme("blue")


def main():
    app = customtkinter.CTk()  # Creating custom tkinter window
    app.geometry("800x600")
    app.title('FaceFury Login')

    def open_upload_image():
        def target():
            subprocess.Popen(["python", "upload_image.py"])
            app.destroy()  # Destroy the app window after starting the subprocess
        threading.Thread(target=target).start()

    def login_user():
        username = entry1.get()
        password = entry2.get()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login successful", "Login Successful!")
            remember_me = var.get()  # Check if "Remember Me" is checked
            if remember_me:
                with open("remember_me.txt", "w") as file:
                    file.write("1")  # Write '1' to indicate that "Remember Me" is checked
            else:
                if os.path.exists("remember_me.txt"):
                    os.remove("remember_me.txt")  # Remove the file if "Remember Me" is unchecked
            open_upload_image()  # Open upload_image.py
        else:
            messagebox.showinfo("Login Failed", "Invalid username or password")
        
        conn.close()  # Close the database connection

    def sign_up_clicked():
        print("Sign Up Clicked")
        app.destroy()
        signup.main()

    
    img1 = ImageTk.PhotoImage(Image.open(r"C:\Users\ROG\Desktop\HCK\FYP\code2\pattern.png"))

    # img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
    l2.place(x=50, y=45)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
    entry1.place(x=50, y=110)

    entry2 = customtkinter.CTkEntry(master=frame, show="*", width=220, placeholder_text="Password")
    entry2.place(x=50, y=160)

    var = IntVar()
    text = "Remember Me"
    checkbox_width = len(text) // 2  # Adjust width based on text length
    checkbox_height = 1  # Adjust height to maintain proportion
    remember_me_checkbox = customtkinter.CTkCheckBox(master=frame, text=text, font=('Century Gothic', 11), variable=var, width=checkbox_width, height=checkbox_height)
    remember_me_checkbox.pack(pady=10)
    remember_me_checkbox.place(x=50, y=197.5)

    # Check if "Remember Me" was checked previously
    try:
        with open("remember_me.txt", "r") as file:
            remember_me_status = int(file.read())
            if remember_me_status == 1:
                remember_me_checkbox.select()
    except FileNotFoundError:
        pass

    button1 = customtkinter.CTkButton(master=frame, width=220, text='login', corner_radius=6, command=login_user)
    button1.place(x=50, y=235)

    l3 = customtkinter.CTkLabel(master=frame, text="Don't have an Account?", font=('Century Gothic', 12))
    l3.place(x=65, y=270)

    button2 = customtkinter.CTkButton(master=frame, width=6, text='Sign up', command=sign_up_clicked, fg_color='transparent')
    button2.place(x=210, y=270)

    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
