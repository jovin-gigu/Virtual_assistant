import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import webbrowser
import pyttsx3
import wikipedia
import qrcode
import speech_recognition as sr
from PIL import Image, ImageTk
import os

LOG_FILE = "logs.txt"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Clear logs on startup
with open(LOG_FILE, "w") as f:
    f.write("")

def speak(text):
    print(f"🎩 Assistant says: {text}")
    engine.say(text)
    engine.runAndWait()

def log_command(command):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] USER: {command}\n")

def log_response(response):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ASSISTANT: {response}\n")

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        voice_status.config(text="🎤 Listening...")
        root.update()
        print("🎤 Listening... Say something")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        command = command.lower()
        print(f"🎩 You said: {command}")
        log_command(command)
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, I didn’t understand that.")
        log_command("[Unrecognized speech]")
        return ""
    except sr.RequestError:
        print("⚠️ Could not request results from Google.")
        log_command("[Speech recognition error]")
        return ""
    finally:
        voice_status.config(text="")
        voice_start_button.pack(pady=10)

def search_wikipedia(query, speak_response=True):
    try:
        result = wikipedia.summary(query, sentences=2)
        log_response(result)
        update_chat(f"You: {query}\nAssistant: {result}")
        if speak_response:
            speak(result)
    except wikipedia.exceptions.DisambiguationError:
        response = f"There are multiple results for {query}. Please be more specific."
        log_response(response)
        update_chat(f"Assistant: {response}")
    except wikipedia.exceptions.PageError:
        response = "I couldn't find the page you asked for."
        log_response(response)
        update_chat(f"Assistant: {response}")
    except Exception as e:
        response = f"An error occurred while searching Wikipedia: {e}"
        log_response(response)
        update_chat(f"Assistant: {response}")

def generate_qr_code(data):
    if not data:
        response = "Please provide valid data to generate a QR code."
        speak(response)
        log_response(response)
        return

    qr = qrcode.make(data)
    path = "qrcode.png"
    qr.save(path)
    response = "QR code has been generated and saved as 'qrcode.png'."
    speak(response)
    log_response(response)
    show_qr_code(path)

def show_qr_code(path):
    qr_window = tk.Toplevel()
    qr_window.title("Generated QR Code")
    img = Image.open(path)
    img = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(qr_window, image=tk_img)
    label.image = tk_img
    label.pack(padx=10, pady=10)

def start_assistant():
    def process_command(command):
        if "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The current time is {now}."
            speak(response)
            log_response(response)
            update_chat(f"You: {command}\nAssistant: {response}")
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            response = "Opening Google."
            speak(response)
            log_response(response)
            update_chat(f"You: {command}\nAssistant: {response}")
        elif "exit" in command or "stop" in command:
            response = "Goodbye! Exiting assistant."
            speak(response)
            log_response(response)
            root.quit()
        elif "wikipedia" in command:
            wikipedia_mode()
        elif "generate qr code" in command:
            data = command.replace("generate qr code", "").strip()
            if data:
                generate_qr_code(data)
            else:
                response = "Please tell me the data to encode in the QR code."
                speak(response)
                log_response(response)
                update_chat(f"You: {command}\nAssistant: {response}")
        elif command:
            response = "Sorry, I didn't understand that command. Try again."
            speak(response)
            log_response(response)
            update_chat(f"You: {command}\nAssistant: {response}")

    def update_chat(text):
        chat_log.config(state="normal")
        chat_log.insert("end", text + "\n\n")
        chat_log.config(state="disabled")
        chat_log.see("end")

    def wikipedia_mode():
        click_frame.pack_forget()
        wiki_frame.pack(fill="both", expand=True)
        chat_log.config(state="normal")
        chat_log.delete("1.0", tk.END)
        chat_log.config(state="disabled")

    def submit_wikipedia_query():
        query = wiki_input.get()
        if query:
            log_command(query)
            update_chat(f"You: {query}")
            try:
                result = wikipedia.summary(query, sentences=2)
                log_response(result)
                update_chat(f"Assistant: {result}")
            except wikipedia.exceptions.DisambiguationError:
                response = f"There are multiple results for {query}. Please be more specific."
                log_response(response)
                update_chat(f"Assistant: {response}")
            except wikipedia.exceptions.PageError:
                response = "I couldn't find the page you asked for."
                log_response(response)
                update_chat(f"Assistant: {response}")
            except Exception as e:
                response = f"An error occurred while searching Wikipedia: {e}"
                log_response(response)
                update_chat(f"Assistant: {response}")
            wiki_input.delete(0, tk.END)

    def manual_qr():
        data = simpledialog.askstring("QR Code", "Enter data to encode:", parent=root)
        if data:
            generate_qr_code(data)

    def open_click_commands():
        main_frame.pack_forget()
        click_frame.pack(fill="both", expand=True)

    def start_voice_command():
        voice_start_button.pack_forget()
        command = listen_command()
        if command:
            process_command(command)

    def open_voice_command():
        main_frame.pack_forget()
        voice_frame.pack(fill="both", expand=True)
        voice_status.config(text="")
        chat_log.config(state="normal")
        chat_log.delete("1.0", tk.END)
        chat_log.config(state="disabled")
        voice_start_button.pack(pady=10)

    def go_back(from_frame):
        from_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
        chat_log.config(state="normal")
        chat_log.delete("1.0", tk.END)
        chat_log.config(state="disabled")

    global root, voice_status, voice_start_button, chat_log, wiki_input

    root = tk.Tk()
    root.title("AI Assistant")
    root.geometry("500x500")

    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    tk.Label(
    main_frame,
    text="Welcome to Your AI Assistant 🤖",
    font=("Helvetica", 18, "bold"),
    fg="#333333"
).pack(pady=(30, 20))

    tk.Button(main_frame, text="🎤 Voice Command", width=20, command=open_voice_command).pack(pady=10)
    tk.Button(main_frame, text="🟡 Click a Command", width=20, command=open_click_commands).pack(pady=10)

    # Click Frame
    click_frame = tk.Frame(root)
    tk.Label(click_frame, text="Click a Command", font=("Arial", 14)).pack(pady=10)
    tk.Button(click_frame, text="🕒 What's the Time", command=lambda: process_command("time")).pack(pady=5)
    tk.Button(click_frame, text="🌐 Open Google", command=lambda: process_command("open google")).pack(pady=5)
    tk.Button(click_frame, text="🔍 Wikipedia Mode", command=wikipedia_mode).pack(pady=5)
    tk.Button(click_frame, text="💰 Generate QR Code", command=manual_qr).pack(pady=5)
    tk.Button(click_frame, text="🔙 Go Back", command=lambda: go_back(click_frame)).pack(pady=20)

    # Voice Frame
    voice_frame = tk.Frame(root)
    tk.Label(voice_frame, text="Voice Command Mode", font=("Arial", 14)).pack(pady=10)
    voice_status = tk.Label(voice_frame, text="", font=("Arial", 12))
    voice_status.pack(pady=10)
    voice_start_button = tk.Button(voice_frame, text="🎤 Start Listening", command=start_voice_command)
    voice_start_button.pack(pady=10)
    chat_log = tk.Text(voice_frame, height=10, width=50, state="disabled", wrap="word")
    chat_log.pack(pady=10)
    tk.Label(voice_frame, text="Available commands:", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(voice_frame, text="- What's the time\n- Open Google\n- Search Wikipedia\n- Generate QR Code\n- Exit", justify="left").pack()
    tk.Button(voice_frame, text="🔙 Go Back", command=lambda: go_back(voice_frame)).pack(pady=20)

    # Wikipedia Frame
    wiki_frame = tk.Frame(root)
    tk.Label(wiki_frame, text="Wikipedia Search Mode", font=("Arial", 14)).pack(pady=10)
    chat_log = tk.Text(wiki_frame, height=10, width=50, state="disabled", wrap="word")
    chat_log.pack(pady=10)
    wiki_input = tk.Entry(wiki_frame, width=40)
    wiki_input.pack(pady=5)
    tk.Button(wiki_frame, text="Search", command=submit_wikipedia_query).pack(pady=5)
    tk.Button(wiki_frame, text="🔙 Go Back", command=lambda: go_back(wiki_frame)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_assistant()
