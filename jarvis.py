import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import datetime

recognizer = sr.Recognizer()
news_api = "Your_newsapi_key"
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": (
                "You are Jarvis, a helpful AI assistant. "
                "You answer questions clearly and concisely, "
                "and you can assist with general tasks like opening apps, "
                "fetching information, and explaining concepts."
            )
        },
        {"role": "user", "content": command}
    ]
)


def processCommand(c):
    # Websites
        if "open google" in c.lower():
            webbrowser.open("https://google.com")
        elif "open youtube" in c.lower():
            webbrowser.open("https://youtube.com")
        elif "open facebook" in c.lower():
            webbrowser.open("https://facebook.com")
        elif "open instagram" in c.lower():
            webbrowser.open("https://instagram.com")
        elif "open x" in c.lower():
            webbrowser.open("https://x.com")
        elif "open gmail" in c.lower():
            webbrowser.open("https://mail.google.com")
        elif "open amazon" in c.lower():
            webbrowser.open("https://amazon.com")
        elif "open netflix" in c.lower():
            webbrowser.open("https://netflix.com")

        # Local apps
        elif "open notepad" in c.lower():
            os.system("notepad")
        elif "open calculator" in c.lower():
            os.system("calc")
        elif "open chrome" in c.lower():
            os.system("start chrome")

        # System info
        elif "time" in c.lower():
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {now}")
        elif "date" in c.lower():
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        # System controls
        elif "shutdown" in c.lower():
            os.system("shutdown /s /t 1")
        elif "restart" in c.lower():
            os.system("shutdown /r /t 1")
        elif "log off" in c.lower():
            os.system("shutdown /l")

        # News headlines
        elif "news" in c.lower():
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                for article in articles[:5]:
                    title = article.get("title")
                    if title:
                        speak(title)
            else:
                speak("Sorry, I couldn't fetch the news.")

        else:
            # Let OpenAI handle the request
            output = aiProcess(c)
            speak(output) 

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()

        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)
            word = r.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("Ya")

                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")

