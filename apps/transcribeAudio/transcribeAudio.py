# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!


import os
from datetime import timedelta

import whisper
import srt

from apps.incFile import increment_filename


def transcribe_audio_files(file_paths:list[str], output_dir:str):
    # Load the Whisper model
    model: whisper.Whisper = whisper.load_model(
        name="turbo", in_memory=True
    )  # Use the second GPU (index 1)

    for file_path in file_paths:
        # Check if the file exists
        if os.path.exists(file_path):
            print("transcribing: ", str(file_path))
            # Transcribe the audio file
            result = model.transcribe(file_path)

            # Create the output file path
            output_txt_file_path = os.path.join(
                output_dir, os.path.basename(file_path) + ".txt"
            )
            output_srt_file_path = os.path.join(
                output_dir, os.path.basename(file_path) + ".srt"
            )
            output_txt_file_path = increment_filename(output_txt_file_path)
            output_srt_file_path = increment_filename(output_srt_file_path)

            print("Generating timestamps for: ", str(file_path))
            segments = []
            for i, segment in enumerate(result["segments"]):
                start = timedelta(seconds=segment["start"])
                end = timedelta(seconds=segment["end"])
                segments.append(
                    srt.Subtitle(
                        index=i + 1, start=start, end=end, content=segment["text"]
                    )
                )

            print("Saving Text for: ", str(file_path))
            with open(output_srt_file_path, "w", encoding="utf-8") as f:
                f.write(srt.compose(segments))

            # Write the transcript to the output file
            with open(output_txt_file_path, "w", encoding="utf-8") as f:
                f.write(str(result["text"]))

            print(f"Transcript saved for {file_path} at {output_txt_file_path}")
            print(f"srt captions for {file_path} at {output_srt_file_path}")
        else:
            print(f"File not found: {file_path}")
