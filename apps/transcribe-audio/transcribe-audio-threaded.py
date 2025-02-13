#!/usr/bin/env transcribe-audio
"""
 # @ Author: Aaron Shackelford
 # @ Create Time: 2025-02-12 14:36:57
 # @ Modified by: Aaron Shackelford
 # @ Modified time: 2025-02-13 08:57:17
 # @ Description: transcribes audio
 """


import os
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor

# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!


# os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Use the second GPU (index 1)
# pip install git+https://github.com/openai/whisper.git
import whisper

MAX_WORKERS = 10

GPU = False


def increment_filename(file_path: str, template: str = " ({counter})") -> str:
    """
    increment_filename increments given file

    Args:
        file_path (str): path to file. will increment if exists
        template (str): python template. Please use `counter` for the increment argument<br>
            Defaults to " ({counter})".<br>
            ex: `' ({counter:03})'` to pad left with zeros.

    Returns:
        str: new file path
    """
    # Split the file path into directory, base name, and extension
    directory, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)

    # Initialize the counter
    counter: int = 1

    # Generate new file name with increment
    while os.path.exists(file_path):
        increment: str = template.replace("{counter}", str(counter))
        new_name: str = f"{name}{increment}{ext}"
        file_path = os.path.join(directory, new_name)
        counter += 1
    return file_path


def transcribe_audio_file(file_path: str, output_dir: str) -> None:
    """
    transcribe_audio_files transcribes audio file

    Args:
        file_paths (str): file to transcribe
        output_dir (str): folder to export to
    """
    # Load the Whisper model
    model: whisper.Whisper = whisper.load_model(
        name="turbo", in_memory=True
    )  # Use the second GPU (index 1)

    # Check if the file exists
    if os.path.exists(file_path):
        # Transcribe the audio file
        result = dict[str, str | list]()
        if GPU:
            result = model.transcribe(audio=file_path)
        else:
            result = model.transcribe(audio=file_path)

        # Create the output file path
        output_file_path = os.path.join(
            output_dir, os.path.basename(file_path) + ".txt"
        )

        output_file_path: str = increment_filename(file_path=output_file_path)

        # Write the transcript to the output file
        with open(file=output_file_path, mode="w", encoding="utf-8") as f:
            f.write(str(result["text"]))

        print(f"Transcript saved for {file_path} at {output_file_path}")
    else:
        print(f"File not found: {file_path}")


def transcribe_audio_file_thread_helper(thread_helper_arguments: list) -> None:
    """
    transcribe_audio_file_thread_helper calls `transcribe_audio_file`

    Args:
        thread_helper_arguments (list): arguments for thread
    """
    transcribe_audio_file(
        file_path=thread_helper_arguments[0], output_dir=thread_helper_arguments[1]
    )


def select_files() -> None:
    file_paths = filedialog.askopenfilenames(
        title="Select Audio Files", filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")]
    )
    files_entry.delete(0, tk.END)
    files_entry.insert(0, ";".join(file_paths))


def select_output_dir() -> None:
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)


def start_transcription() -> None:
    file_paths = files_entry.get().split(";")
    output_dir = output_entry.get()

    if not file_paths or not output_dir:
        messagebox.showerror(
            "Error", "Please select audio files and an output directory."
        )
        return

    thread_helper_list = list()
    for file in file_paths:
        thread_helper_list.append([file, output_dir])

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(transcribe_audio_file_thread_helper, thread_helper_list)
    messagebox.showinfo("Success", "Transcription completed!")


# Create the main window
root = tk.Tk()
root.title("Audio Transcription")

# Create and place the widgets
tk.Label(root, text="Select Audio Files:").grid(row=0, column=0, padx=10, pady=10)
files_entry = tk.Entry(root, width=50)
files_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_files).grid(
    row=0, column=2, padx=10, pady=10
)

tk.Label(root, text="Select Output Directory:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_dir).grid(
    row=1, column=2, padx=10, pady=10
)

tk.Button(root, text="Start Transcription", command=start_transcription).grid(
    row=2, column=0, columnspan=3, pady=20
)

# Run the application
root.mainloop()
