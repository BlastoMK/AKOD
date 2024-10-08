import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the image files
bg_image_path = os.path.join(script_dir, 'bg.jpg')

def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def connect_database():
    if (email := emailEntry.get()) == "" or (username := usernameEntry.get()) == "" or (password := passwordEntry.get()) == "" or (confirm := confirmEntry.get()) == "":
        messagebox.showerror("Error", "All fields are required")
    elif password != confirm:
        messagebox.showerror("Error!", "Password Mismatch")
    elif check.get() == 0:
        messagebox.showerror("Error", "Please accept Terms & Conditions")
    else:
        try:
            # Connect to the database
            con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="userdata")
            mycursor = con.cursor()

            # Check if username already exists
            query = "SELECT * FROM data WHERE username = %s"
            mycursor.execute(query, (username,))
            row = mycursor.fetchone()

            if row is not None:
                messagebox.showerror("Error!", "Username Already Exists")
            else:
                # Insert data into the table
                query = "INSERT INTO data(email, username, password) VALUES (%s, %s, %s)"
                mycursor.execute(query, (email, username, password))

                # Commit changes and close connection
                con.commit()
                con.close()

                # Show success message and clear the entries
                messagebox.showinfo("Success", "Registration is Successful")
                clear()
                signup_window.destroy()
                import login
        except pymysql.Error as e:
            messagebox.showerror("Error!", f"Database Error: {e}")

def login_page():
    signup_window.destroy()
    import login

signup_window = Tk()
signup_window.title("Signup Page")
signup_window.resizable(False, False)
background = ImageTk.PhotoImage(file=bg_image_path)

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window, bg="white")
frame.place(x=554, y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=("Microsoft Yahei UI Light", 18, "bold")
                , bg="white", fg="firebrick1")
heading.grid(row=0, column=0)

emailLabel = Label(frame, text="Email", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white"
                   , fg="firebrick")
emailLabel.grid(row=1, column=0, sticky="w", padx=25, pady=(10, 0))

emailEntry = Entry(frame, width=30, font=("Microsoft Yahei UI Light", 10, "bold"),
                   fg="white", bg="firebrick1")
emailEntry.grid(row=2, column=0, sticky="w", padx=25)

usernameLabel = Label(frame, text="Username", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white"
                      , fg="firebrick")
usernameLabel.grid(row=3, column=0, sticky="w", padx=25, pady=(10, 0))

usernameEntry = Entry(frame, width=30, font=("Microsoft Yahei UI Light", 10, "bold"),
                      fg="white", bg="firebrick1")
usernameEntry.grid(row=4, column=0, sticky="w", padx=25)

passwordLabel = Label(frame, text="Password", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white"
                      , fg="firebrick")
passwordLabel.grid(row=5, column=0, sticky="w", padx=25, pady=(10, 0))

passwordEntry = Entry(frame, width=30, font=("Microsoft Yahei UI Light", 10, "bold"),
                      fg="white", bg="firebrick1")
passwordEntry.grid(row=6, column=0, sticky="w", padx=25)

confirmLabel = Label(frame, text="Confirm Password", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white"
                     , fg="firebrick")
confirmLabel.grid(row=7, column=0, sticky="w", padx=25, pady=(10, 0))

confirmEntry = Entry(frame, width=30, font=("Microsoft Yahei UI Light", 10, "bold"),
                     fg="white", bg="firebrick1")
confirmEntry.grid(row=8, column=0, sticky="w", padx=25)
check = IntVar()
termsandconditions = Checkbutton(frame, text="I agree to the terms and conditions", font=("Microsoft Yahei UI Light", 9, "bold")
                                 , fg="firebrick1", bg="white", activebackground="white", activeforeground="firebrick1",
                                 cursor="hand2", variable=check)
termsandconditions.grid(row=9, column=0, pady=10, padx=15)

signupButton = Button(frame, text="Sign Up", font=("Open Sans", 16, "bold"), bd=0, bg="firebrick1", fg="white", activebackground="firebrick1", activeforeground="white",
                      width=17, command=connect_database)
signupButton.grid(row=10, column=0, pady=10)

alreadyaccount = Label(frame, text="Already have an Account?", font=("Open Sans", 9, "bold"), bg="white"
                       , fg="firebrick")
alreadyaccount.grid(row=11, column=0, sticky="w", padx=25, pady=10)

loginButton = Button(frame, text="Log in", font=("Open Sans", 9, "bold underline"),
                     bg="white", fg="blue", bd=0, cursor="hand2", activebackground="white",
                     activeforeground="blue", command=login_page)
loginButton.place(x=175, y=382)

signup_window.mainloop()
