import tkinter as tk
from tkinter import messagebox, Menu
from tkinter import ttk
from PIL import ImageTk
import pymysql
import os
import subprocess

def get_script_path(script_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, script_name)

login_script_path = get_script_path("login.py")
excel_script_path = get_script_path("excel.py")

root = tk.Tk()
root.geometry('800x600')
root.title("TkinterHub")

# Function to check admin status from a file
def check_admin_status():
    try:
        with open("user_info.txt", "r") as f:
            lines = f.read().strip().split("\n")
            for line in lines:
                if line:
                    email, role = line.split(",")
                    return role.strip() == "admin"
    except FileNotFoundError:
        return False
    except ValueError:
        return False

is_admin = check_admin_status()

def switch(indicator_lb, page):
    for child in options_fm.winfo_children():
        if isinstance(child, tk.Label):
            child["bg"] = "SystemButtonFace"
    indicator_lb["bg"] = "#0097e8"
    for fm in main_fm.winfo_children():
        fm.destroy()
        root.update()
    page()

def logout():
    root.destroy()
    subprocess.run(['python', login_script_path])

def about_us():
    messagebox.showinfo("About Us", "This is the About Us section.")

def settings():
    messagebox.showinfo("Settings", "This is the Settings section.")

def fetch_data():
    con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="rmu_excel")
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM excel_document ORDER BY Number")
    data = mycursor.fetchall()
    con.close()
    return data

def execute_sql_query(query):
    try:
        con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="userdata")
        mycursor = con.cursor()
        mycursor.execute(query)
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Query executed successfully")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Database Error: {e}")

def admin_feature():
    if is_admin:
        query = """CREATE TABLE IF NOT EXISTS new_table (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL
                    );"""
        execute_sql_query(query)
    else:
        messagebox.showwarning("Permission Denied", "You do not have admin privileges")

options_fm = tk.Frame(root)

home_btn = tk.Button(options_fm, text="Home", font=("Arial", 13), bd=0, fg="#0097e8", activeforeground="#0097e8",
                     command=lambda: switch(indicator_lb=home_indicator_lb, page=home_page))
home_btn.place(x=0, y=0, width=125)

home_indicator_lb = tk.Label(options_fm, bg="#0097e8")
home_indicator_lb.place(x=22, y=30, width=80, height=2)

product_indicator_lb = tk.Label(options_fm)
product_indicator_lb.place(x=247, y=30, width=80, height=2)

contact_indicator_lb = tk.Label(options_fm)
contact_indicator_lb.place(x=422, y=30, width=80, height=2)

# Dropdown menu button
menu_btn = tk.Menubutton(options_fm, text="⋮", font=("Arial", 20), relief=tk.FLAT, direction=tk.RIGHT)
menu = Menu(menu_btn, tearoff=0)
menu.add_command(label="About Us", command=about_us)
menu.add_command(label="Settings", command=settings)
menu.add_separator()
menu.add_command(label="Admin Feature", command=admin_feature)
menu.add_separator()
menu.add_command(label="Logout", command=logout)
menu_btn.config(menu=menu)
menu_btn.place(x=750, y=0, width=50)

options_fm.pack(pady=15)
options_fm.pack_propagate(False)
options_fm.configure(width=800, height=35)

def home_page():
    home_page_fm = tk.Frame(main_fm)
    canvas = tk.Canvas(home_page_fm)
    scrollbar = tk.Scrollbar(home_page_fm, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    # Table headers
    headers = ["Edit", "Number", "Receiver", "REF", "Origin", "Date on Letter", "File No",
               "Date Received", "Subject", "Processing Officer", "Action Officer", 
               "Date Marked", "Days Taken to Mark", "Response Date", "Days Taken to Respond", 
               "Comments", "Date of Dispatch"]
    
    for col_num, header in enumerate(headers):
        label = tk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), fg="#0097e8", anchor="w")
        label.grid(row=0, column=col_num, padx=5, pady=5)
    
    data = fetch_data()
    for i, row in enumerate(data):
        edit_btn = tk.Button(scrollable_frame, text="Edit", font=("Arial", 10), fg="#0097e8", command=lambda r=row: edit_row(r))
        edit_btn.grid(row=i + 1, column=0, padx=5, pady=5)

        for j, value in enumerate(row):
            label = tk.Label(scrollable_frame, text=value, font=("Arial", 10), fg="#0097e8", anchor="w")
            label.grid(row=i + 1, column=j + 1, padx=5, pady=5)

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")
    home_page_fm.pack(fill=tk.BOTH, expand=True)

def edit_row(row):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Row")

    fields = ["Number", "Receiver", "REF", "Origin", "Date on Letter", "File No",
              "Date Received", "Subject", "Processing Officer", "Action Officer", 
              "Date Marked", "Days Taken to Mark", "Response Date", "Days Taken to Respond", 
              "Comments", "Date of Dispatch"]

    entry_widgets = []

    for i, field in enumerate(fields):
        label = tk.Label(edit_window, text=field, font=("Arial", 10))
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(edit_window, font=("Arial", 10))
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry.insert(0, row[i])
        entry_widgets.append(entry)

    def save_changes():
        updated_values = [widget.get() for widget in entry_widgets]
        try:
            con = pymysql.connect(host="localhost", user="root", password="Sage_mode2", database="rmu_excel")
            mycursor = con.cursor()
            query = """UPDATE excel_document SET 
                       number=%s, receiver=%s, ref=%s, origin=%s, date_on_letter=%s, file_no=%s, 
                       date_received=%s, subject=%s, processing_officer=%s, action_officer=%s, 
                       date_marked=%s, days_taken_to_mark=%s, response_date=%s, 
                       days_taken_to_respond=%s, comments=%s, date_of_dispatch=%s 
                       WHERE number=%s"""
            updated_values.append(row[0])
            mycursor.execute(query, updated_values)
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Row updated successfully")
            edit_window.destroy()
            switch(indicator_lb=home_indicator_lb, page=home_page)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    save_btn = tk.Button(edit_window, text="Save", font=("Arial", 10), command=save_changes)
    save_btn.grid(row=len(fields), column=1, pady=10)

def open_excel_script():
    subprocess.Popen(['python', excel_script_path])

main_fm = tk.Frame(root)
main_fm.pack(fill=tk.BOTH, expand=True)

def refresh_data():
    switch(indicator_lb=home_indicator_lb, page=home_page)

home_page()

excel_btn = tk.Button(root, text="Open Data Entry Excel", font=("Arial", 10), fg="#0097e8", command=open_excel_script)
excel_btn.pack(pady=10)

refresh_btn = tk.Button(root, text="Refresh Data", font=("Arial", 10), fg="#0097e8", command=refresh_data)
refresh_btn.pack(pady=10)

root.mainloop()
