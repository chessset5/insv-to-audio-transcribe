import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from apps.misc.FileNameFunctions import increment_filename


# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

# Function to extract audio from video files
def extract_audio(video_path: str, output_folder: str) -> str:
    # Define the output audio file path
    audio_path = os.path.join(
        output_folder, os.path.splitext(os.path.basename(video_path))[0] + ".wav"
    )
    audio_path: str = increment_filename(file_path=audio_path)
    path : str = r"ffmpeg"
    if os.name == 'nt':
        # Windows
        path = r".\apps\misc\bin\win64\ffmpeg\bin\ffmpeg.exe"
    # elif os.name == 'posix':
    #     if os.uname().sysname == 'Darwin':
    #         # macOS
    #         path = "/path/to/macos/directory"
    #     else:
    #         # Linux/Unix
    #         path = "/path/to/linux/directory"

    # Run ffmpeg command to extract audio
    subprocess.run(
        args=[path, "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True
    )

    print(f"Completed extraction for: {video_path}")
    return audio_path


# Function to start the extraction process
def start_extraction(video_files: list[str], output_folder: str) -> None | list[str]:

    if not video_files or not output_folder:
        print("Error", "Please select video files and an output folder.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Use ThreadPoolExecutor to run multiple extractions simultaneously
    with ThreadPoolExecutor() as executor:
        result: os.Iterator[str] = executor.map(
            lambda video_file: extract_audio(video_path=video_file, output_folder=output_folder), video_files
        )

    print("Success", "Audio extraction completed for files:\n", str(object=video_files))
    return list(result)
