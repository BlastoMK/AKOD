import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the image
image_path = os.path.join(script_dir, "MTPW.png")

# Construct the full path to the login script
login_script_path = os.path.join(script_dir, "login.py")

# Create a splash screen
root = tk.Tk()
root.geometry("600x400")
root.overrideredirect(1)  # Remove window decorations (title bar, etc.)

# Load the splash screen image
try:
    splash_image = Image.open(image_path)
    splash_photo = ImageTk.PhotoImage(splash_image)
    splash_label = tk.Label(root, image=splash_photo)
    splash_label.pack()
except Exception as e:
    print(f"Error loading splash screen image: {e}")
    root.destroy()
    sys.exit(1)

# Function to proceed to the login screen
def proceed_to_login():
    root.destroy()
    subprocess.run(['python', login_script_path])

# Set a timer to close the splash screen and open the login screen
root.after(5000, proceed_to_login)  # Show splash screen for 5 seconds

root.mainloop()
