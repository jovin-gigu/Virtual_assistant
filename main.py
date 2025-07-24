import tkinter as tk
from tkinter import messagebox
from login import LoginWindow

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("900x500")
        self.root.minsize(800, 400)
        self.dark_mode = False

        self.top_bar = tk.Frame(self.root, bg="gray", height=10)
        self.top_bar.pack(side="top", fill="x")

        self.theme_toggle_btn = tk.Button(
            self.top_bar,
            text="🌙",
            command=self.toggle_theme,
            bg="#f27935",
            fg="white",
            bd=0,
            relief="raised"
        )
        self.theme_toggle_btn.pack(side="right", padx=10, pady=2)

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.show_login()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.current_frame and hasattr(self.current_frame, "apply_theme"):
            self.current_frame.apply_theme()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = LoginWindow(
            parent=self.container,
            controller=self,
            login_callback=self.on_login_success
        )
        self.current_frame.pack(fill="both", expand=True)
        self.apply_theme()

    def on_login_success(self, username):
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        self.root.destroy()
        from assistant2 import start_assistant
        start_assistant()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
