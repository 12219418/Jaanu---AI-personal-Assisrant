import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import sys
import sounddevice as sd
import numpy as np
import time

# NLP
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------
# INIT
# -------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def talk(text):
    print(f"Jaanu: {text}")
    engine.say(text)
    engine.runAndWait()

nlp = spacy.load("en_core_web_sm")

# -------------------------
# INTENT MODEL
# -------------------------
training_data = [
    ("play song", "PLAY_MUSIC"),
    ("play music", "PLAY_MUSIC"),
    ("play telugu song", "PLAY_MUSIC"),

    ("search google", "SEARCH_WEB"),
    ("find something", "SEARCH_WEB"),

    ("who is elon musk", "WIKIPEDIA"),
    ("what is machine learning", "WIKIPEDIA"),
    ("tell me about virat kohli", "WIKIPEDIA"),

    ("what time is it", "GET_TIME"),

    ("exit", "EXIT"),
]

texts = [x[0] for x in training_data]
labels = [x[1] for x in training_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

def detect_intent(text):
    return model.predict(vectorizer.transform([text]))[0]

# -------------------------
# ENTITY EXTRACTION
# -------------------------
def extract_entity(text):
    doc = nlp(text)

    for ent in doc.ents:
        return ent.text

    # fallback cleanup
    noise = ["play", "song", "music", "search", "google", "who is", "what is"]
    for word in noise:
        text = text.replace(word, "")

    return text.strip()

# -------------------------
# AUDIO INPUT
# -------------------------
def take_command():
    recognizer = sr.Recognizer()
    samplerate = 16000
    duration = 3

    print("Listening...")

    try:
        audio = sd.rec(int(samplerate * duration),
                       samplerate=samplerate,
                       channels=1,
                       dtype='int16')
        sd.wait()

        audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)
        command = recognizer.recognize_google(audio_data)

        print("You:", command)
        return command.lower()

    except:
        print("Didn't catch that")
        return ""

# -------------------------
# ACTIONS
# -------------------------
def play_music(entity):
    if not entity:
        talk("What should I play?")
        return

    talk(f"Playing {entity}")
    pywhatkit.playonyt(entity)

def search_google(entity):
    if not entity:
        talk("What should I search?")
        return

    talk(f"Searching {entity}")
    webbrowser.open(f"https://www.google.com/search?q={entity}")

def search_wikipedia(entity):
    try:
        results = wikipedia.search(entity)

        if not results:
            talk("No results found")
            return

        summary = wikipedia.summary(results[0], sentences=2)
        talk(summary)

    except Exception:
        talk("Opening in browser instead")
        webbrowser.open(f"https://en.wikipedia.org/wiki/{entity}")

def get_time():
    time_now = datetime.datetime.now().strftime('%I:%M %p')
    talk(f"Time is {time_now}")

# -------------------------
# ROUTER
# -------------------------
def handle_command(command):
    intent = detect_intent(command)
    entity = extract_entity(command)

    print("Intent:", intent)
    print("Entity:", entity)

    if intent == "PLAY_MUSIC":
        play_music(entity)

    elif intent == "SEARCH_WEB":
        search_google(entity)

    elif intent == "WIKIPEDIA":
        search_wikipedia(entity)

    elif intent == "GET_TIME":
        get_time()

    elif intent == "EXIT":
        talk("Goodbye")
        sys.exit()

    else:
        talk("I don't understand")

# -------------------------
# RUN
# -------------------------
talk("NLP Assistant started")

while True:
    cmd = take_command()
    if cmd:
        handle_command(cmd)
    time.sleep(0.5)
