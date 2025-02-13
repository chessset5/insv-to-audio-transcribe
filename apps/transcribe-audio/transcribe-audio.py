import tkinter as tk
from tkinter import filedialog, messagebox

# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!


import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Use the second GPU (index 1)
# pip install git+https://github.com/openai/whisper.git
import whisper


def transcribe_audio_files(file_paths, output_dir):
    # Load the Whisper model
    model: whisper.Whisper = whisper.load_model(
        name="turbo", in_memory=True
    )  # Use the second GPU (index 1)

    for file_path in file_paths:
        # Check if the file exists
        if os.path.exists(file_path):
            # Transcribe the audio file
            result = model.transcribe(file_path)

            # Create the output file path
            output_file_path = os.path.join(
                output_dir, os.path.basename(file_path) + ".txt"
            )

            # Write the transcript to the output file
            with open(output_file_path, "w") as f:
                f.write(str(result["text"]))

            print(f"Transcript saved for {file_path} at {output_file_path}")
        else:
            print(f"File not found: {file_path}")


def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Audio Files", filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")]
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
