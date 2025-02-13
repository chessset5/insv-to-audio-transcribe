#!/usr/bin/env transcribe-audio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# make sure to make .env copy from .env-example
load_dotenv()

# Retrieve the file path
audio_path: str | None = os.getenv("TEST_AUDIO_FILE_PATH")

# Example from:
# https://github.com/openai/whisper?tab=readme-ov-file#python-usage
import whisper

model = whisper.load_model("turbo")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(file=audio_path)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)
