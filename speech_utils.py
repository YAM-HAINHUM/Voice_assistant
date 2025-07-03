# speech_utils.py
import pyttsx3
import speech_recognition as sr

def init_tts_engine(language="en"):
    engine = pyttsx3.init()
    # You can customize voices based on language here if available
    # Some voices support multiple languages, else fallback to default
    voices = engine.getProperty('voices')
    # Simple example: pick first voice, or extend for multi-lang support
    engine.setProperty('voice', voices[0].id)
    return engine

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

def listen(language="en"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        # language param supported by Google Speech API
        text = r.recognize_google(audio, language=language)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
    except sr.RequestError:
        print("Speech recognition API unavailable.")
        return ""
