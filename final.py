import cv2
import RPi.GPIO as GPIO
from time import sleep
import spacy
import datetime
import pyttsx3
import requests
import json
import pygame
import speech_recognition as sr
import re

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")
API_KEY = "AIzaSyCQSiO6USRVFv_v5xm8Tae9Pk3REKsCCMY"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

pygame.mixer.init()

# Define GPIO pins
ypin = 11
xpin = 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(xpin, GPIO.OUT)
GPIO.setup(ypin, GPIO.OUT)

x = GPIO.PWM(xpin, 50)
y = GPIO.PWM(ypin, 50)

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
    engine.setProperty('rate', rate-50)
    voices = engine.getProperty('voices')
    voice_id = voices[17].id  # Changed to use the first voice in the list
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {current_date}")

def query_gemini(user_query):
    headers={'Content-Type':'application/json'}
    data={"contents":[{"parts":[{"text":user_query}]}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        try:
            text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            text = re.sub(r'[^a-zA-Z0-9 ,.]', '', text)
            return text
        except (KeyError, IndexError):
            print("Error parsing response JSON")
            return ""
    else:
        print(f"Request error: {response.status_code}")
        print(f"HTTP error: {response.text}")
        return ""

def play_music():
    music_file = "/home/disala/Desktop/Little London Girl(lyrics).mp3"
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def process_query(query):
    doc = nlp(query)
    
    if "time" in query and "now" in query or "what time is it" in query:
        return "time"
    elif "date" in query and "now" in query or "what day is it" in query:
        return "date"
    elif "introduction" in query and "you" in query:
        return "introduction"
    elif "who" in query and ("make" in query or "create" in query) and "you" in query:
        return "disala"
    elif "play" in query and ("music" in query or "song" in query):
        return "music"
    elif any(word in query for word in ['what', 'who', 'which', 'when', 'how', 'why', 'solve', 'tell']):
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
        #speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        speak("Could not request results; {0}".format(e))
        return ""

def mains():
    wishme()
    while True:
        query = take_command().lower()
        if query:
            intent = process_query(query)
            
            if intent == "time":
                get_time()
            elif intent == "date":
                get_date()
            elif intent == "disala":
                speak("Disala is the one who created me for his course project.")
            elif intent == "introduction":
                speak("I am Sparky. Disala is the one who created me for his course project.")
            elif intent == "question":
                speak("Searching...")
                gemini_response = query_gemini(query + ' give answer as a summary, only as a paragraph. dont use any  brackets or anything like that')
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
            elif len(query) > 7 or query == "":
                speak("I didn't understand what you are asking.")

class servopos():
    def __init__(self):
        self.currentx, self.currenty = 7, 4
        x.start(self.currentx)
        y.start(self.currenty)
        sleep(1)
        x.ChangeDutyCycle(0)
        y.ChangeDutyCycle(0)

    def setposx(self, diffx):
        self.currentx += diffx
        self.currentx = round(self.currentx, 2)
        if 0 < self.currentx < 15:
            x.ChangeDutyCycle(self.currentx)
            sleep(0.02)
            x.ChangeDutyCycle(0)

    def setposy(self, diffy):
        self.currenty += diffy
        self.currenty = round(self.currenty, 2)
        if 0 < self.currenty < 15:
            y.ChangeDutyCycle(self.currenty)
            sleep(0.02)
            y.ChangeDutyCycle(0)

    def setdcx(self, dcx):
        x.ChangeDutyCycle(dcx)

    def setdcy(self, dcy):
        y.ChangeDutyCycle(dcy)

ser = servopos()

cascade_path = '/home/disala/Desktop/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

Px, Ix, Dx = -1/160, 0, 0
Py, Iy, Dy = -0.2/120, 0, 0

integral_x, integral_y = 0, 0
differential_x, differential_y = 0, 0
prev_x, prev_y = 0, 0
width, height = 320, 240

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
sleep(0.1)

def face_detected():
    print("Face detected!")
    mains()

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        frame = cv2.flip(frame, 1)
        
        ser.setdcx(0)
        ser.setdcy(0)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        c = 0
        for (fx, fy, fw, fh) in faces:
            c += 1
            if c > 1:  # We just take care of the first face detected
                break
            
            face_centre_x = fx + fw / 2
            face_centre_y = fy + fh / 2
            
            error_x = 160 - face_centre_x
            error_y = 120 - face_centre_y
            
            global integral_x, integral_y, differential_x, differential_y, prev_x, prev_y
            integral_x += error_x
            integral_y += error_y
            
            differential_x = prev_x - error_x
            differential_y = prev_y - error_y
            
            prev_x = error_x
            prev_y = error_y
            
            valx = Px * error_x + Dx * differential_x + Ix * integral_x
            valy = Py * error_y + Dy * differential_y + Iy * integral_y
            
            valx = round(valx, 2)
            valy = round(valy, 2)
            
            if abs(error_x) < 20:
                ser.setdcx(0)
            else:
                if abs(valx) > 0.5:
                    sign = valx / abs(valx)
                    valx = 0.5 * sign
                ser.setposx(valx)
            
            if abs(error_y) < 20:
                ser.setdcy(0)
            else:
                if abs(valy) > 0.5:
                    sign = valy / abs(valy)
                    valy = 0.5 * sign
                ser.setposy(valy)
            
            frame = cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 6)
            
            # Call the function when a face is detected
            face_detected()
        
        # Display the frame
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF
        
        # If the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

if __name__ == "__main__":
    main()
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
