import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
from tkinter import ttk
import os
import random
import string

USER_FILE = "users.json"
SESSION_FILE = "session.json"

# Load or initialize user database
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        user_credentials = json.load(f)
else:
    user_credentials = {}
    with open(USER_FILE, "w") as f:
        json.dump(user_credentials, f)

def save_credentials():
    with open(USER_FILE, "w") as f:
        json.dump(user_credentials, f)

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def validate_login(username, password):
    return username in user_credentials and user_credentials[username] == password

def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username", "")
    return ""

class LoginWindow(tk.Frame):
    def __init__(self, parent, controller, login_callback):
        super().__init__(parent)
        self.controller = controller
        self.login_callback = login_callback

        self.username = tk.StringVar(value=load_session())
        self.password = tk.StringVar()
        self.new_username = tk.StringVar()
        self.new_password = tk.StringVar()
        self.password_mode = tk.StringVar(value="manual")
        self.remember_me = tk.BooleanVar(value=True)

        self.login_frame = tk.Frame(self)
        self.signup_frame = tk.Frame(self)

        self.build_login_frame()
        self.build_signup_frame()

        self.login_frame.pack(fill="both", expand=True)

    def add_placeholder(self, entry, placeholder_text, is_password=False):
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg="#000000")
                if is_password:
                    entry.config(show="*")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg="#a9a9a9")
                if is_password:
                    entry.config(show="")

        entry.insert(0, placeholder_text)
        entry.config(fg="#a9a9a9")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        if is_password:
            entry.config(show="")

    def switch_frame(self, to_signup):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        if to_signup:
            self.signup_frame.pack(fill="both", expand=True)
        else:
            self.login_frame.pack(fill="both", expand=True)

    def load_image(self, parent):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "assets", "example.png")
            print("Loading image from:", image_path)  # Debug

            img = Image.open(image_path)
            img = img.resize((500, 500), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(parent, image=photo, bg="#ffffff")
            img_label.image = photo
            img_label.pack(expand=True, fill="both")
        except Exception as e:
            print("Error loading image:", e)
            tk.Label(parent, text="Image\nPlaceholder", font=("Arial", 20), bg="#cccccc", fg="#555555").pack(expand=True)


    def build_login_frame(self):
        frame = self.login_frame
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=11)
        frame.grid_columnconfigure(1, weight=5)

        left = tk.Frame(frame, bg="#ffffff")
        left.grid(row=0, column=0, sticky="nsew")
        self.load_image(left)

        self.right_login = tk.Frame(frame, padx=20, pady=20)
        self.right_login.grid(row=0, column=1, sticky="nsew")
        self.right_login.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.right_login, text="Login 🔒", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0, 20))

        self.username_entry = tk.Entry(self.right_login, textvariable=self.username, font=("Arial", 11), width=30)
        self.username_entry.pack(pady=8, ipady=6)
        self.add_placeholder(self.username_entry, "Username")

        self.password_entry = tk.Entry(self.right_login, textvariable=self.password, font=("Arial", 11), width=30)
        self.password_entry.pack(pady=8, ipady=6)
        self.add_placeholder(self.password_entry, "Password", is_password=True)

        self.remember_checkbox = tk.Checkbutton(self.right_login, text="Remember me", variable=self.remember_me)
        self.remember_checkbox.pack(anchor="w", pady=(10, 20))

        self.login_btn = tk.Button(
        self.right_login,
        text="Login",
        command=self.attempt_login,
        padx=4,
        pady=5,
        width=15,
        font=("Helvetica", 12, "bold")  # Increased font size
        )
        self.login_btn.pack(pady=(0, 10))


        self.create_account_btn = tk.Label(self.right_login, text="Create Account", font=("Arial", 10, "underline"), fg="#007bff", cursor="hand2")
        self.create_account_btn.pack(pady=(5, 20))
        self.create_account_btn.bind("<Button-1>", lambda e: self.switch_frame(True))

    def build_signup_frame(self):
        frame = self.signup_frame
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=11)
        frame.grid_columnconfigure(1, weight=5)

        left = tk.Frame(frame, bg="#ffffff")
        left.grid(row=0, column=0, sticky="nsew")
        self.load_image(left)

        self.right_signup = tk.Frame(frame, padx=20, pady=20)
        self.right_signup.grid(row=0, column=1, sticky="nsew")
        self.right_signup.columnconfigure(0, weight=1)

        self.signup_title = tk.Label(self.right_signup, text="Create Account 📝", font=("Helvetica", 19, "bold"))
        self.signup_title.pack(pady=(0, 30))

        self.new_username_entry = tk.Entry(self.right_signup, textvariable=self.new_username, font=("Arial", 11), width=30)
        self.new_username_entry.pack(pady=5, ipady=6)
        self.add_placeholder(self.new_username_entry, "Username")

        tk.Radiobutton(self.right_signup, text="Enter password manually", variable=self.password_mode, value="manual").pack(anchor="w", pady=(15, 0))
        self.new_password_entry = tk.Entry(self.right_signup, textvariable=self.new_password, font=("Arial", 11), width=30)
        self.new_password_entry.pack(pady=5, ipady=6)
        self.add_placeholder(self.new_password_entry, "Password", is_password=True)

        tk.Radiobutton(self.right_signup, text="Generate strong password", variable=self.password_mode, value="generate").pack(anchor="w", pady=(10, 20))

        self.signup_btn = tk.Button(self.right_signup, text="Create Account", command=self.create_account, padx=7, pady=5, width=20,font=("Helvetica", 11, "bold"))
        self.signup_btn.pack(pady=10)

        self.back_to_login_lbl = tk.Label(
            self.right_signup,
            text="🔙 Back to Login",
            font=("Arial", 10, "underline"),
            fg="#007bff",
            cursor="hand2",
            bg=self.right_signup["bg"]
        )
        self.back_to_login_lbl.pack()
        self.back_to_login_lbl.bind("<Button-1>", lambda e: self.switch_frame(False))


    def apply_theme(self):
        dark = self.controller.dark_mode
        bg = "#222" if dark else "#f8f8f8"
        fg = "#f0f0f0" if dark else "#000"
        entry_bg = "#333" if dark else "#fff"
        btn_bg = "#f27935"
        btn_fg = "#fff"

        for frame in [self.right_login, getattr(self, 'right_signup', None)]:
            if frame:
                frame.configure(bg=bg)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Checkbutton, tk.Radiobutton)):
                        widget.configure(bg=bg, fg=fg)
                    elif isinstance(widget, tk.Entry):
                        widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
                    elif isinstance(widget, tk.Button):
                        widget.configure(bg=btn_bg, fg=btn_fg, activebackground="#d9651c", relief="flat")

    def attempt_login(self):
        username = self.username.get()
        password = self.password.get()
        if validate_login(username, password):
            if self.remember_me.get():
                save_session(username)
            elif os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
            self.login_callback(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def create_account(self):
        username = self.new_username.get()
        mode = self.password_mode.get()

        if username in user_credentials:
            messagebox.showerror("Error", "Username already exists.")
            return

        if mode == "generate":
            try:
                length_str = simpledialog.askstring("Password Length", "Enter password length:")
                length = int(length_str)
                password = generate_password(length)
                messagebox.showinfo("Generated Password", f"Your password: {password}")
            except:
                messagebox.showerror("Error", "Invalid password length.")
                return
        else:
            password = self.new_password.get()
            if not password:
                messagebox.showerror("Error", "Please enter a password.")
                return

        user_credentials[username] = password
        save_credentials()
        messagebox.showinfo("Success", "Account created! You can now log in.")
        self.switch_frame(False)
