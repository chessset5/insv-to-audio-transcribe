#!/usr/bin/env transcribe-audio
from operator import mod
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# make sure to make .env copy from .env-example
load_dotenv()

# Retrieve the file path
AUDIO_PATH: str | None = os.getenv("TEST_AUDIO_FILE_PATH")
STR_PATH: str | None = os.getenv("TEST_TEXT_FILE_PATH")

import whisper
import srt
from datetime import timedelta



def transcribe_to_srt(input_audio: str, output_srt: str, model_size: str = "medium") -> None:
    """
    Transcribe an audio file using OpenAI Whisper and save the output as an SRT file.

    Args:
        input_audio (str): Path to the input audio file.
        output_srt (str): Path to save the output SRT file.
        model_size (str, optional): Whisper model size (e.g., "small", "medium", "large"). Defaults to "medium".
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(input_audio)

    segments = []
    for i, segment in enumerate(result["segments"]):
        start = timedelta(seconds=segment["start"])
        end = timedelta(seconds=segment["end"])
        segments.append(srt.Subtitle(index=i + 1, start=start, end=end, content=segment["text"]))

    with open(output_srt, "w", encoding="utf-8") as f:
        f.write(srt.compose(segments))

    print(f"Transcription saved to: {output_srt}")

# Example usage:
# transcribe_to_srt("audio.mp3", "output.srt")
if AUDIO_PATH and STR_PATH:
    transcribe_to_srt(input_audio=AUDIO_PATH,output_srt=STR_PATH,model_size="turbo")