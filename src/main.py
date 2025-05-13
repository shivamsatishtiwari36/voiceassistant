import os
import json
import io
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from google.cloud import speech

# Load environment variables
load_dotenv()

# Initialize Google STT client
client = speech.SpeechClient()

# Text-to-speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Listen function using Google STT
def listen():
    print("Starting to listen...")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    print("Audio captured.")

    # Save to temp.wav
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

    with io.open("temp.wav", "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,  # Match with your mic
        language_code="en-IN"
    )

    try:
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            transcript = result.alternatives[0].transcript
            print("You said:", transcript)
            return transcript.lower()
    except Exception as e:
        print("Google STT Error:", e)
        return ""

# Load dataset
def load_data():
    try:
        with open("res.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading res.json:", e)
        return None

# Recommend restaurant
def recommend_restaurant(query, data):
    matches = []
    for r in data["restaurants_and_cafes"]:
        for cuisine in r["cuisine"]:
            if cuisine.lower() in query:
                matches.append(r)
                break

    if matches:
        top = matches[0]
        recommendation = f"I recommend {top['name']} located at {top['location']}. They serve {', '.join(top['cuisine'])} cuisine."
        print("Recommended:", recommendation)
        speak(recommendation)
    else:
        print("Recommended: No recommendations found")
        speak("Sorry, I couldn't find a matching restaurant.")

# Main function
if __name__ == "__main__":
    print("Script is running")
    query = listen()
    if query:
        data = load_data()
        if data:
            recommend_restaurant(query, data)
        else:
            speak("Sorry, I could not load the restaurant data.")
    else:
        speak("Sorry, I did not catch that.")
