# === FILE: voice_assistant.py ===
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import smtplib
import time
import threading
import json
import pywhatkit
from config import EMAIL, PASSWORD, WAKE_WORD, LANGUAGE
from reminder_manager import add_reminder, list_reminders, cancel_reminder, reminder_checker
from calendar_manager import create_event, list_today_events
from nlp_utils import extract_entities
from speech_utils import speak, init_tts_engine
from jokes_trivia import get_random_joke, get_random_trivia
from location_reminder import LocationReminder
from emotion_detection import predict_emotion
from location_utils import get_current_location
from gui_dashboard import AssistantDashboard
from cache_utils import cache_response, get_cached_response
from logger_util import log_info, log_error
import tkinter as tk
import os

# -------------------- Setup --------------------
with open("custom_commands.json") as f:
    custom_commands = json.load(f)

engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def load_banned_keywords(file_path="banned_keywords.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    except FileNotFoundError:
        print("⚠️ banned_keywords.txt not found. No filtering will be applied.")
        return []

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I help you?")

# -------------------- Voice Recognition --------------------
def take_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🔊 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            with open("last_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
    except Exception as mic_error:
        print(f"❌ Microphone error: {mic_error}")
        speak("Microphone issue detected.")
        return ""

    try:
        print("🧠 Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"🗣️ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Can you repeat?")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is not available.")
        return ""

# -------------------- Other Functionalities --------------------
def send_email(to_address, subject, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        message = f"Subject: {subject}\n\n{content}"
        server.sendmail(EMAIL, to_address, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print("Email Error:", e)

def get_weather(city):
    api_key = " "
    base_url = " "
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        try:
            main = data['main']
            weather_desc = data['weather'][0]['description']
            temp = main['temp']
            humidity = main['humidity']
            city_name = data.get('name', city)
            return (f"The weather in {city_name} is currently {weather_desc} "
                    f"with temperature {temp} degree Celsius and humidity {humidity} percent.")
        except (KeyError, IndexError):
            return "Sorry, there was an error processing the weather data."
    else:
        return "Sorry, I couldn't get the weather information right now."

def set_reminder(message, minutes):
    def reminder():
        time.sleep(minutes * 60)
        speak(f"Reminder: {message}")
    threading.Thread(target=reminder).start()

# -------------------- Main Assistant Function --------------------
def run_assistant():
    wish_user()
    banned_words = load_banned_keywords()
    reminder_checker(speak)

    while True:
        command = take_command()
        if not command:
            continue

        cmd = command.lower()
        print(f"📥 Command: {cmd}")

        if any(word in cmd for word in banned_words):
            speak("Sorry, I cannot respond to that request.")
            continue

        if "stop" in cmd or "exit" in cmd:
            speak("Goodbye!")
            break

        elif "time" in cmd:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "date" in cmd:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")

        elif "send email" in cmd:
            speak("Please type the recipient's email address:")
            to = input("Recipient Email: ")
            speak("What is the subject?")
            subject = take_command()
            speak("What should I say?")
            body = take_command()
            speak("Do you want me to send the email now?")
            confirm = take_command()
            if "yes" in confirm:
                send_email(to, subject, body)
            else:
                speak("Okay, the email was not sent.")

        elif "weather" in cmd:
            speak("Which city?")
            city = take_command()
            if city:
                try:
                    weather_report = get_weather(city)
                    speak(weather_report)
                except Exception as e:
                    speak("There was a problem fetching the weather.")
                    print("❌ Weather Error:", e)
            else:
                speak("Sorry, I didn't get the city name.")

        elif "set reminder" in cmd:
            speak("What should I remind you about?")
            reminder_msg = take_command()
            speak("In how many minutes?")
            try:
                minutes = int(take_command())
                reminder_id = add_reminder(reminder_msg, minutes)
                speak(f"Reminder set: '{reminder_msg}' in {minutes} minutes.")
                print(f"⏰ Reminder ID: {reminder_id}")
            except ValueError:
                speak("Sorry, I didn't understand the number of minutes.")

        elif "add event" in cmd or "add meeting" in cmd:
            speak("What is the event about?")
            summary = take_command()
            if not summary:
                speak("Sorry, I didn't get the event details.")
                continue
            speak("Please type the date and time in format 'YYYY-MM-DD HH:MM'")
            start_time = input("Enter date and time (YYYY-MM-DD HH:MM): ")
            speak(f"You said: Event '{summary}' at {start_time}. Do you want me to add it?")
            confirmation = take_command()
            if "yes" in confirmation:
                try:
                    event_link = create_event(summary, start_time)
                    speak("Event added successfully.")
                    print("📅 Event Link:", event_link)
                except Exception as e:
                    speak("Sorry, I couldn't add the event.")
                    print("❌ Event Creation Error:", e)
            else:
                speak("Okay, I won’t add the event.")

        elif any(phrase in cmd for phrase in ["what's on calendar", "what's on my calendar", "today's events", "calendar events", "google calendar"]):
            events = list_today_events()
            if not events:
                speak("You have no events today.")
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    speak(f"{event['summary']} at {start}")

        elif "who is" in cmd or "what is" in cmd or "tell me about" in cmd:
            speak("Let me check...")
            answer = ask_wolfram(command)
            if "Sorry" in answer or not answer:
                answer = ask_wikipedia(command)
            speak(answer)

        elif "play music" in cmd or "play song" in cmd:
            speak("Which song should I play?")
            song = take_command()
            if song:
                speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)
            else:
                speak("I didn't catch the song name.")

        elif "analyze" in cmd:
            entities = extract_entities(command)
            if entities:
                entity_list = ", ".join(f"{text} ({label})" for text, label in entities)
                speak(f"I found these entities: {entity_list}")
            else:
                speak("I didn't find any specific entities.")

        elif "where am i" in cmd or "what's my location" in cmd or "current location" in cmd:
            try:
                location = get_current_location()
                if location:
                    city = location.get("city", "Unknown")
                    region = location.get("region", "")
                    country = location.get("country", "")
                    speak(f"You are currently in {city}, {region}, {country}.")
                else:
                    speak("Sorry, I couldn't determine your location.")
            except Exception as e:
                speak("There was a problem retrieving your location.")
                print("❌ Location Error:", e)

        elif command in custom_commands:
            speak(custom_commands[command])

        else:
            speak("I'm still learning. Would you like me to search the web?")

# -------------------- WolframAlpha and Wikipedia --------------------
def ask_wolfram(question):
    import wolframalpha
    WOLFRAM_APP_ID = "QJRG4A-4PL2KUUK37"
    wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)
    try:
        res = wolfram_client.query(question)
        answer = next(res.results).text
        return answer
    except Exception:
        return "Sorry, I couldn't find an answer."

def ask_wikipedia(question):
    import wikipedia
    try:
        summary = wikipedia.summary(question, sentences=2)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Your question is ambiguous. Did you mean: {e.options[0]}?"
    except Exception:
        return "Sorry, I couldn't find an answer."

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    run_assistant()
