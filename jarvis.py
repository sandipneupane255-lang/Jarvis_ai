import datetime
import os
import webbrowser

import pygame
import pyttsx3
import requests
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI

recognizer = sr.Recognizer()


def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    if not os.getenv("OPENAI_API_KEY"):
        return "Set the OPENAI_API_KEY environment variable to use AI responses."

    client = OpenAI()
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
                ),
            },
            {"role": "user", "content": command},
        ],
    )
    return completion.choices[0].message.content or "I couldn't create a response."


def confirm_system_action(action):
    confirmation = f"CONFIRM {action.upper()}"
    typed = input(f"Type '{confirmation}' in this console to proceed: ").strip().upper()
    return typed == confirmation


def processCommand(c):
    command = c.lower()

    # Websites
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
    elif "open x" in command:
        webbrowser.open("https://x.com")
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
    elif "open amazon" in command:
        webbrowser.open("https://amazon.com")
    elif "open netflix" in command:
        webbrowser.open("https://netflix.com")

    # Local apps
    elif "open notepad" in command:
        os.system("notepad")
    elif "open calculator" in command:
        os.system("calc")
    elif "open chrome" in command:
        os.system("start chrome")

    # System info
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    # Power actions require confirmation typed into the console.
    elif "shutdown" in command:
        if confirm_system_action("shutdown"):
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown cancelled.")
    elif "restart" in command:
        if confirm_system_action("restart"):
            os.system("shutdown /r /t 1")
        else:
            speak("Restart cancelled.")
    elif "log off" in command:
        if confirm_system_action("log off"):
            os.system("shutdown /l")
        else:
            speak("Log off cancelled.")

    # News headlines
    elif "news" in command:
        news_api_key = os.getenv("NEWSAPI_API_KEY")
        if not news_api_key:
            speak("Set the NEWSAPI_API_KEY environment variable to fetch news.")
            return

        try:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "us", "apiKey": news_api_key},
                timeout=10,
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])
            if articles:
                for article in articles[:5]:
                    title = article.get("title")
                    if title:
                        speak(title)
            else:
                speak("No headlines are available right now.")
        except requests.RequestException:
            speak("Sorry, I couldn't fetch the news.")

    else:
        speak(aiProcess(c))


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()

        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
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
