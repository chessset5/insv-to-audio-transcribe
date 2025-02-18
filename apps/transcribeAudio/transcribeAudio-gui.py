#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from transcribeAudio import transcribe_audio_files

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_path not in sys.path:
    sys.path.append(project_path)


from apps.misc.GlobalVariables import ACCEPTABLE_AUDIO_FILE_TYPES


def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Audio Files", filetypes=ACCEPTABLE_AUDIO_FILE_TYPES
    )
    files_entry.delete(0, tk.END)
    files_entry.insert(0, ";".join(file_paths))


def select_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)


def start_transcription():
    file_paths = files_entry.get().split(";")
    output_dir = output_entry.get()

    if not file_paths or not output_dir:
        messagebox.showerror(
            "Error", "Please select audio files and an output directory."
        )
        return

    transcribe_audio_files(file_paths, output_dir)
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
