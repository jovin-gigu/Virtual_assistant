import speech_recognition as sr
import datetime
import webbrowser
import os
import pyttsx3  # Text-to-speech library
import wikipedia  # Wikipedia search library
import qrcode  # QR code generation library

LOG_FILE = "logs.txt"

# Initialize the pyttsx3 engine for TTS
engine = pyttsx3.init()

# Function to speak the response out loud
def speak(text):
    print(f"🗣️ Assistant says: {text}")  # Print to console for reference
    engine.say(text)  # Speak the text
    engine.runAndWait()  # Wait until the speech is done

# Function to write spoken command to logs.txt
def log_command(command):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {command}\n")

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening... Say something")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        command = command.lower()
        print(f"🗣️ You said: {command}")
        log_command(command)  # Log the spoken command
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, I didn’t understand that.")
        log_command("[Unrecognized speech]")
        return ""
    except sr.RequestError:
        print("⚠️ Could not request results from Google.")
        log_command("[Speech recognition error]")
        return ""

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia, {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Sorry, there are multiple results for {query}. Please be more specific.")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("Sorry, I couldn't fetch information from Wikipedia.")
    except wikipedia.exceptions.RedirectError:
        speak("Sorry, I couldn't find the page you asked for.")

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("qrcode.png")
    speak("QR code generated and saved as qrcode.png.")

def start_assistant():
    speak("Assistant started. Say a command, like what's the time, search Wikipedia, or generate a QR code.")

    while True:
        command = listen_command()

        if "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Current time is {now}")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google...")

        elif "exit" in command or "stop" in command:
            speak("Goodbye! Exiting Assistant.")
            print("👋 Assistant exiting. Goodbye!")
            break

        elif "search wikipedia" in command:
            query = command.replace("search wikipedia", "").strip()
            if query:
                search_wikipedia(query)
            else:
                speak("Please provide a search term after 'search Wikipedia'.")

        elif "generate qr code" in command:
            data = command.replace("generate qr code", "").strip()
            if data:
                generate_qr_code(data)
            else:
                speak("Please provide data to generate the QR code.")

        elif command:
            speak("Command not recognized. Please try again.")
            print("🤖 Command not recognized. Try again.")
