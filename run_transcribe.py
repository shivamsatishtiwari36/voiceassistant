from src.api.speech_to_text import transcribe_audio

result = transcribe_audio("Conference.wav")  # Replace with your exact file name if different
print("Transcription:\n", result)
