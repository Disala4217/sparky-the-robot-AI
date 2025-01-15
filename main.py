import spacy
import datetime
import pyttsx3
import requests
import json
import pygame
import speech_recognition as sr

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")
API_KEY = "AIzaSyBOXYHnVv6_Bkp619iaRt_slyo4iSXz6_o"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

pygame.mixer.init()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-70)
    voices = engine.getProperty('voices')
    voice_id = voices[0].id  # Changed to use the first voice in the list
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

def time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {current_date}")

def query_gemini(user_query):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": {
            "text": user_query
        }
    }

    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        try:
            text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except (KeyError, IndexError):
            print("Error parsing response JSON")
            return ""
    else:
        print(f"Request error: {response.status_code}")
        print(f"HTTP error: {response.text}")
        return ""

def play_music():
    music_file = "/home/disala/Music/y2mate.com - Shawn Mendes  Mercy Official Music Video.mp3"
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def process_query(query):
    doc = nlp(query)
    
    if "time" in query and "now" in query:
        return "time"
    elif "date" in query and "now" in query:
        return "date"
    elif "introduction" in query and "you" in query:
        return "introduction"
    elif "who" in query and ("make" in query or "create" in query) and "you" in query:
        return "disala"
    elif "play" in query and ("music" in query or "song" in query):
        return "music"
    elif any(word in query for word in ['what', 'who', 'which', 'when', 'how', 'why', 'solve']):
        return "question"
    else:
        return "unknown"

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        speak("Could not request results; {0}".format(e))
        return ""

def main():
    wishme()
    while True:
        query = take_command().lower()
        if query:
            intent = process_query(query)
            
            if intent == "time":
                time()
            elif intent == "date":
                date()
            elif intent == "disala":
                speak("Disala is the one who created me for his course project.")
            elif intent == "introduction":
                speak("I am Sparky. Disala is the one who created me for his course project.")
            elif intent == "question":
                speak("Searching...")
                gemini_response = query_gemini(query + " give answer as a summary, only as a paragraph. dont use any commas brackets or anything like that")
                if gemini_response:
                    print(f"You: {query}")
                    print(f"Gemini: {gemini_response}")
                    speak(gemini_response)
                else:
                    print("Failed to retrieve response from Gemini.")
                    speak("Failed to retrieve response from Gemini.")
            elif intent == "music":
                speak("Playing music.")
                play_music()
            elif "exit" in query or "quit" in query:
                speak("Goodbye!")
                break
            else:
                speak("I didn't understand what you are asking.")

if __name__ == "__main__":
    main()
