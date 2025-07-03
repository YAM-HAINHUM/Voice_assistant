import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import json
import os

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Custom Commands Path
CUSTOM_COMMANDS_FILE = "custom_commands.json"

# Helper Functions
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to microphone and return recognized speech."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Please speak your full command clearly.")
        try:
            # Wait max 10 seconds for the user to start speaking
            # Once they start, allow up to 30 seconds to speak
            audio = r.listen(source, timeout=10, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            speak("No voice detected. Please try again.")
            return ""
    print("Analyzing...")
    try:
        query = r.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error. Please check your internet.")
    return ""


def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")

def search_web(query):
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather(city="Pune"):
    api_key = "a1e556292e2f1491ecb74db01142b00b"  # Replace with your valid API key
    city = city.title().strip()  # Format city name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url).json()
        print("API response:", resp)  # Debug output
        if resp.get("cod") == 200:
            temp = resp["main"]["temp"]
            desc = resp["weather"][0]["description"]
            speak(f"It's {temp} °C with {desc} in {city}")
        else:
            error_msg = resp.get("message", "City not found.")
            speak(f"Error: {error_msg}")
    except Exception as e:
        speak("Unable to get weather data right now.")
        print("Weather API error:", e)

def ask_city():
    """Ask user for city name until valid input is received."""
    for _ in range(3):
        speak("Which city would you like the weather for?")
        city = listen()
        if city:
            return city
        else:
            speak("Sorry, I didn't hear the city name.")
    speak("Let's skip weather for now.")
    return None

def load_custom_commands():
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        with open(CUSTOM_COMMANDS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_custom_command(trigger, response):
    commands = load_custom_commands()
    commands[trigger.lower()] = response
    with open(CUSTOM_COMMANDS_FILE, "w") as f:
        json.dump(commands, f, indent=4)

def handle_custom_command(cmd):
    commands = load_custom_commands()
    for trigger, response in commands.items():
        if trigger in cmd:
            speak(response)
            return True
    return False

def main():
    speak("Voice assistant activated. How can I help you?")
    while True:
        cmd = listen()
        if not cmd:
            continue

        if handle_custom_command(cmd):
            continue

        if "hello" in cmd:
            speak("Hello! How can I assist you today?")
        elif "time" in cmd:
            tell_time()
        elif "date" in cmd:
            tell_date()
        elif "search" in cmd:
            term = cmd.replace("search", "").strip()
            if term:
                search_web(term)
            else:
                speak("Please tell me what to search for.")
        elif "weather" in cmd:
            city = ask_city()
            if city:
                get_weather(city)
        elif cmd.startswith("add command"):
            speak("Please say the trigger phrase for your new command.")
            trigger = listen()
            if trigger:
                speak("Now say the response I should give.")
                response = listen()
                if response:
                    save_custom_command(trigger, response)
                    speak("Custom command saved.")
        elif any(word in cmd for word in ["exit", "quit", "bye"]):
            speak("Goodbye! Stay safe.")
            break
        else:
            speak("Sorry, I didn't understand that. Try again.")

if __name__ == "__main__":
    main()
