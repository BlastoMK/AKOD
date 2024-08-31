import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
import subprocess
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the image files
bg_image_path = os.path.join(script_dir, 'bg.jpg')
background_image_path = os.path.join(script_dir, 'background.jpg')
openeye_image_path = os.path.join(script_dir, 'openeye.png')
closeye_image_path = os.path.join(script_dir, 'closeye.png')

# Functionality Part
def forget_pass():
    def change_password():
        if user_entry.get() == "" or newpass_entry.get() == "" or confirmpass_entry.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=window)
        elif newpass_entry.get() != confirmpass_entry.get():
            messagebox.showerror("Error", "Password and Confirm Password are not matching", parent=window)
        else:
            con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="userdata")
            mycursor = con.cursor()
            query = "select * from data where username=%s"
            mycursor.execute(query, (user_entry.get(),))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Incorrect Username", parent=window)
            else:
                query = "update data set password=%s where username=%s"
                mycursor.execute(query, (newpass_entry.get(), user_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Password is reset, Please login with the new password", parent=window)
                window.destroy()

    window = Toplevel()
    window.title("Change Password")

    bgPic = ImageTk.PhotoImage(file=background_image_path)
    bgLabel = Label(window, image=bgPic)
    bgLabel.image = bgPic  # Keep a reference to the image to prevent garbage collection
    bgLabel.grid()

    heading_label = Label(window, text="RESET PASSWORD", font=("arial", "18", "bold"), bg="white", fg="magenta2")
    heading_label.place(x=480, y=60)

    userLabel = Label(window, text="Username", font=("arial", 12, "bold"), bg="white", fg="orchid1")
    userLabel.place(x=470, y=130)

    user_entry = Entry(window, width=25, font=("arial", 11, "bold"), bd=0, fg="magenta2")
    user_entry.place(x=470, y=160)

    Frame(window, width=250, height=2, bg="orchid1").place(x=470, y=180)

    passwordLabel = Label(window, text="New Password", font=("arial", 12, "bold"), bg="white", fg="orchid1")
    passwordLabel.place(x=470, y=210)

    newpass_entry = Entry(window, width=25, font=("arial", 11, "bold"), bd=0, fg="magenta2")
    newpass_entry.place(x=470, y=240)

    Frame(window, width=250, height=2, bg="orchid1").place(x=470, y=260)

    confirmpassLabel = Label(window, text="Confirm Password", font=("arial", 12, "bold"), bg="white", fg="orchid1")
    confirmpassLabel.place(x=470, y=290)

    confirmpass_entry = Entry(window, width=25, font=("arial", 11, "bold"), bd=0, fg="magenta2")
    confirmpass_entry.place(x=470, y=320)

    Frame(window, width=250, height=2, bg="orchid1").place(x=470, y=340)

    submitButton = Button(window, text="Submit", font=("Open Sans", 16, "bold"), fg="white", bg="magenta2", activeforeground="white", activebackground="magenta2", cursor="hand2", bd=0, width=19, command=change_password)
    submitButton.place(x=470, y=390)

    window.mainloop()

def login_user():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error!", "All fields are required")
    else:
        try:
            # Connect to the database
            con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="userdata")
            mycursor = con.cursor()

            # Execute the login query
            query = "SELECT * FROM data WHERE username=%s AND password=%s"
            mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))

            # Fetch the first row
            row = mycursor.fetchone()

            # Check if a row was returned
            if row is not None:
                # Login successful
                messagebox.showinfo("Success", "Login successful")
                # Check the user's role
                role = row[3]  # Assuming the 4th column is 'role'
                # Save the user's info to a file
                with open("user_info.txt", "w") as f:
                    f.write(f"{row[0]}\n{role}")  # Assuming the 1st column is 'email'
                # Close the current login window
                login_window.destroy()
                # Open the home.py page using subprocess
                home_script_path = get_script_path("home.py")
                try:
                    logging.info(f"Attempting to run: {home_script_path}")
                    result = subprocess.run(['python', home_script_path], capture_output=True, text=True)
                    logging.info(f"Subprocess call finished with return code {result.returncode}")
                    logging.info(f"Subprocess stdout: {result.stdout}")
                    logging.error(f"Subprocess stderr: {result.stderr}")
                except Exception as e:
                    logging.error(f"Failed to run subprocess: {e}")
            else:
                # Invalid username or password
                messagebox.showerror("Error", "Invalid username or password")

            # Close the connection
            con.close()
        except pymysql.Error as e:
            # Handle database errors
            messagebox.showerror("Error", f"Database Error: {e}")
            logging.error(f"Database Error: {e}")

def get_script_path(script_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, script_name)

def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file=closeye_image_path)
    passwordEntry.config(show="*")
    eyeButton.config(command=show)

def show():
    openeye.config(file=openeye_image_path)
    passwordEntry.config(show="")
    eyeButton.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == "Username":
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == "Password":
        passwordEntry.delete(0, END)

# GUI Part
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title("Login Page")
bgImage = ImageTk.PhotoImage(file=bg_image_path)

bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=("Microsoft Yahei UI Light", 23, "bold"), bg="white", fg="firebrick1")
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="firebrick1")
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, "Username")

usernameEntry.bind("<FocusIn>", user_enter)

frame1 = Frame(login_window, width=250, height=2, bg="firebrick1")
frame1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="firebrick1")
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, "Password")

passwordEntry.bind("<FocusIn>", password_enter)

frame2 = Frame(login_window, width=250, height=2, bg="firebrick1")
frame2.place(x=580, y=282)

openeye = PhotoImage(file=openeye_image_path)
eyeButton = Button(login_window, image=openeye, bd=0, bg="white", activebackground="white", cursor="hand2", command=hide)
eyeButton.place(x=800, y=255)

forgetButton = Button(login_window, text="Forgot Password?", bd=0, bg="white", activebackground="white", cursor="hand2", font=("Microsoft Yahei UI Light", 9, "bold"), fg="firebrick1", activeforeground="firebrick1", command=forget_pass)
forgetButton.place(x=715, y=295)

loginButton = Button(login_window, text="Login", font=("Open Sans", 16, "bold"), fg="white", bg="firebrick1", activeforeground="white", activebackground="firebrick1", cursor="hand2", bd=0, width=19, command=login_user)
loginButton.place(x=578, y=350)

newaccButton = Button(login_window, text="Sign Up", font=("Open Sans", 9, "bold underline"), fg="blue", bg="white", activeforeground="blue", activebackground="firebrick1", cursor="hand2", bd=0, command=signup_page)
newaccButton.place(x=727, y=500)

login_window.mainloop()
