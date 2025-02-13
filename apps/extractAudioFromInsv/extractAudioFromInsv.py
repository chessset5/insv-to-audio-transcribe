import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox

from apps.incFile import increment_filename


# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!


# Function to extract audio from video files
def extract_audio(video_path, output_folder):
    # Define the output audio file path
    audio_path = os.path.join(
        output_folder, os.path.splitext(os.path.basename(video_path))[0] + ".wav"
    )

    audio_path = increment_filename(audio_path)

    # Run ffmpeg command to extract audio
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True
    )

    print(f"Completed extraction for: {video_path}")
    return audio_path


# Function to start the extraction process
def start_extraction(video_files, output_folder):
    if not video_files or not output_folder:
        messagebox.showerror("Error", "Please select video files and an output folder.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Use ThreadPoolExecutor to run multiple extractions simultaneously
    with ThreadPoolExecutor() as executor:
        result = executor.map(
            lambda video_file: extract_audio(video_file, output_folder), video_files
        )

    messagebox.showinfo("Success", "Audio extraction completed for all files.")
    return list(result)


# Function to select video files
def select_files():
    files = filedialog.askopenfilenames(filetypes=[("Video Files", "*.insv")])
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
