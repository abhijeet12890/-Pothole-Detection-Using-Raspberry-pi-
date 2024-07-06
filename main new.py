from tkinter import *
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox as tmsg
from PIL import Image, ImageTk
import cv2
from predictions import detection, draw_bounding_boxes
import time
import os

def animate_login():
    for i in range(20):  # Adjust the range and sleep duration for desired animation
        login_window.update_idletasks()
        login_window.after(50)  # 50 milliseconds
        login_window.geometry(f"800x{600 + i * 5}")

def login_page():
    global main_window, login_window
    login_window = Tk()
    login_window.geometry("800x600")
    login_window.title("Pothole Detection/Login")
    login_window.configure(bg="lightblue")  # Set a background color

    # Create a themed style
    style = ThemedStyle(login_window)
    style.set_theme("plastik")  # You can try different themes

    username_label = ttk.Label(login_window, text="Username:", style="TLabel")
    username_label.pack(pady=20)

    username_entry = ttk.Entry(login_window, style="TEntry")
    username_entry.pack(pady=10)

    password_label = ttk.Label(login_window, text="Password:", style="TLabel")
    password_label.pack(pady=20)

    password_entry = ttk.Entry(login_window, show="*", style="TEntry")
    password_entry.pack(pady=10)

    def validate_login():
        if username_entry.get() == "admin" and password_entry.get() == "admin":
            animate_login()  # Add animation before destroying the login window
            login_window.destroy()
            root.deiconify()
        else:
            tmsg.showerror("Login Failed", "Invalid username or password")

    login_button = ttk.Button(login_window, text="Login", command=validate_login, style="TButton")
    login_button.pack(pady=20)

    login_window.mainloop()

# ... (rest of your code)


def print_path():
    global f
    f = tkinter.filedialog.askopenfilename(
        parent=root,
        initialdir='',
        title='Select file',
        filetypes=[('JPG Image', '*.jpg'), ('MP4 Video', '*.mp4')]
    )
    img1 = cv2.imread(f)
    newimg = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    newimg = cv2.resize(newimg, (512, 512))
    img = Image.fromarray(newimg)
    imgtk = ImageTk.PhotoImage(image=img)
    x.imgtk = imgtk
    x.configure(image=imgtk)

def detect_objects():
    
    if f.endswith('.jpg'):
        img = cv2.imread(f)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        co_ords = detection(img)
        img_new = img.copy()
        detected_img = draw_bounding_boxes(co_ords, img_new)
        detected_img = cv2.resize(detected_img,(512,512))
        img = Image.fromarray(detected_img)
        imgtk = ImageTk.PhotoImage(image=img)
        x.imgtk = imgtk
        x.configure(image=imgtk)

    if f.endswith('.mp4'):
        cap = cv2.VideoCapture(f)

        while True:
            current_time = time.localtime()
            formatted_time = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
            ret, frame = cap.read()
            if not ret:
                break
            co_ords = detection(frame)
            img_new = frame.copy()
            detected_img = draw_bounding_boxes(co_ords, img_new)
            detected_img = cv2.resize(detected_img, (512, 512))
            if co_ords != None:
                if not os.path.exists('screenshots'):
                    os.makedirs('screenshots')
                cv2.imwrite(f'screenshots/{formatted_time}.jpg',detected_img)
            img = Image.fromarray(cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            x.imgtk = imgtk
            x.configure(image=imgtk)
            x.update()


def login_page():
    global main_window
    login_window = Tk()
    login_window.geometry("800x600")
    login_window.title("Pothole Detection/Login")
    login_window.configure(bg="lightblue")  # Set a background color

    # Create a themed style
    style = ThemedStyle(login_window)
    style.set_theme("scidgreen")  # You can try different themes

    username_label = ttk.Label(login_window, text="Username:", style="TLabel")
    username_label.pack(pady=20)

    username_entry = ttk.Entry(login_window, style="TEntry")
    username_entry.pack(pady=10)

    password_label = ttk.Label(login_window, text="Password:", style="TLabel")
    password_label.pack(pady=20)

    password_entry = ttk.Entry(login_window, show="*", style="TEntry")
    password_entry.pack(pady=10)

    def validate_login():
        if username_entry.get() == "admin" and password_entry.get() == "admin":
            # tmsg.showinfo("Login", "Login successful!")
            login_window.destroy()
            root.deiconify()
        else:
            tmsg.showerror("Login Failed", "Invalid username or password")

    login_button = ttk.Button(login_window, text="Login", command=validate_login, style="TButton")
    login_button.pack(pady=20)

    login_window.mainloop()

def live_detection():
    cap = cv2.VideoCapture(0)
    while True:
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
        ret, frame = cap.read()
        if not ret:
            break
        co_ords = detection(frame)
        img_new = frame.copy()
        detected_img = draw_bounding_boxes(co_ords, img_new)
        detected_img = cv2.resize(detected_img,(512,512))
        if co_ords != None:
                if not os.path.exists('Potholes Detected'):
                    os.makedirs('Potholes Detected')
                cv2.imwrite(f'Potholes Detected/{formatted_time}.jpg',detected_img)
        img = Image.fromarray(cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        x.imgtk = imgtk
        x.configure(image=imgtk)
        x.update()
            
root = Tk()
root.geometry("800x800")
root.title("Pothole Detection")
root.resizable(0, 0)
im = None

MF = Frame(root, bd=8, bg="lightgray", relief=GROOVE)
MF.place(x=0, y=0, height=50, width=800)

menu_label = Label(MF, text="Pothole Detection", font=("times new roman", 20, "bold"), bg="lightgrey", fg="black", pady=0)
menu_label.pack(side=TOP, fill="x")

x = Label(root, image=im)
x.grid(row=1, column=0, padx=5, pady=50)

# Create a frame for buttons
button_frame = Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

# "Select Image" button
b1 = Button(button_frame, font=("times new roman", 20, "bold"), text='Select Image/Video', command=print_path, bg="orange", activebackground="darkorange")
b1.grid(row=0, column=0, padx=10)


# "Detect" button
b2 = Button(button_frame, font=("times new roman", 20, "bold"), text='Detect', command=detect_objects, bg="red", activebackground="darkred")
b2.grid(row=0, column=1, padx=10)


#Live button
b2 = Button(button_frame, font=("times new roman", 20, "bold"), text='Live', command=live_detection, bg="green", activebackground="darkred")
b2.grid(row=0, column=2, padx=10)


# Hide the main window initially
root.withdraw()

# Show the login page
login_page()

root.mainloop()
