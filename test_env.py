import os
from google.cloud import speech, texttospeech
from openai import OpenAI
print("Google Cloud and OpenAI setup successful!")
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("OPENAI_API_KEY:", "Set" if os.getenv("OPENAI_API_KEY") else "Not set")