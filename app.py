import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        query = recognizer.recognize_google(audio)
        return query
    except:
        return "Sorry, I could not understand."

def run_jannu(query):
    query = query.lower()

    if "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        reply = f"The current time is {time}"
    
    elif "youtube" in query:
        reply = "Opening YouTube…"
        webbrowser.open("https://youtube.com")
    
    elif "google" in query:
        reply = "Opening Google…"
        webbrowser.open("https://google.com")

    elif "music" in query:
        reply = "Playing music 🎶"
        webbrowser.open("https://www.youtube.com/watch?v=2Vv-BfVoq4g")

    elif "hello" in query:
        reply = "Hello! How can I help you today?"

    elif "your name" in query:
        reply = "My name is Jannu, your personal assistant!"

    else:
        reply = "Sorry, I didn't understand that."

    return reply

# -------------------- STREAMLIT UI --------------------

st.title("🎙️ Jannu – Your Personal Voice Assistant")

st.write("Upload your voice and I will respond back!")

audio_file = st.file_uploader("Upload a voice command (.wav)", type=["wav"])

if audio_file:
    with open("user_input.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    st.audio("user_input.wav")

    st.info("Processing...")

    # Speech to Text
    query = take_command("user_input.wav")
    st.success(f"🧑‍💬 You said: **{query}**")

    # Assistant Response
    reply = run_jannu(query)

    st.write(f"🤖 **Jannu:** {reply}")

    # Text to Speech output
    engine.save_to_file(reply, "reply_output.mp3")
    engine.runAndWait()

    st.audio("reply_output.mp3")
