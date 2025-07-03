# jokes_trivia.py
import random

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and it said 'No problem — I'll go to sleep.'",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

TRIVIA = [
    "Did you know? Honey never spoils. Archaeologists have eaten 3000-year-old honey and found it delicious.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. It lasted between 38 and 45 minutes.",
    "Octopuses have three hearts."
]

def get_random_joke():
    return random.choice(JOKES)

def get_random_trivia():
    return random.choice(TRIVIA)

def load_banned_keywords():
    try:
        with open("banned_keywords.txt", "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    except:
        return []

def filter_text(text):
    banned = load_banned_keywords()
    return not any(word in text.lower() for word in banned)

def get_random_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything.",
        "This is a dangerous joke about murder and bombs."  # example
    ]
    jokes = list(filter(filter_text, jokes))
    return random.choice(jokes) if jokes else "Sorry, no safe jokes available."
