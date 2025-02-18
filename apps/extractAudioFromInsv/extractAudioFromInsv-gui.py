#!/usr/bin/env python3

import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_path not in sys.path:
    sys.path.append(project_path)

import tkinter as tk
from tkinter import filedialog, messagebox

import extractAudioFromInsv
from apps.misc.GlobalVariables import ACCEPTABLE_VIDEO_FILE_TYPES


# Function to start the extraction process
def start_extraction(video_files: list[str], output_folder: str) -> None | list[str]:
    if not video_files or not output_folder:
        messagebox.showerror("Error", "Please select video files and an output folder.")
        return

    extractAudioFromInsv.start_extraction(
        video_files=video_files, output_folder=output_folder
    )

    messagebox.showinfo("Success", "Audio extraction completed for all files.")
    return


# Function to select video files
def select_files():
    file_types = ACCEPTABLE_VIDEO_FILE_TYPES
    files = filedialog.askopenfilenames(filetypes=file_types)
    file_list.delete(0, tk.END)
    for file in files:
        file_list.insert(tk.END, file)


# Function to select output folder
def select_output_folder():
    folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder)


# Create the main window
root = tk.Tk()
root.title("Audio Extraction Tool")

# Create and place the widgets
tk.Label(root, text="Select Video Files:").grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_files).grid(
    row=0, column=1, padx=10, pady=10
)

file_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
file_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Select Output Folder:").grid(row=2, column=0, padx=10, pady=10)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_folder).grid(
    row=3, column=1, padx=10, pady=10
)

tk.Button(
    root,
    text="Start Extraction",
    command=lambda: start_extraction(
        file_list.get(0, tk.END), output_folder_entry.get()
    ),
).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
print("Please Wait for the GUI to Load!")
root.mainloop()
