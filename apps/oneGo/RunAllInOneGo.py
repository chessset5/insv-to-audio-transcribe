import os
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor

from apps.extractAudioFromInsv.extractAudioFromInsv import start_extraction

def run_audio_extract(file: str):
    directory = os.path.dirname(file)
    

def run_scripts(file_paths: list[str]) -> None:
    """Placeholder function to process selected files."""

    with ThreadPoolExecutor() as executor:
        result = executor.map(run_audio_extract, file_paths)


def select_files() -> None:
    """Open a file dialog for selecting .insv files and pass them to run_scripts."""
    file_paths = filedialog.askopenfilenames(
        filetypes=[("INSTA360 Video Files", "*.insv")]
    )
    if file_paths:
        run_scripts(list(file_paths))


def main() -> None:
    """Create the Tkinter GUI."""
    root = tk.Tk()
    root.title("INSV File Selector")
    root.geometry("300x150")

    btn_select = tk.Button(root, text="Select INSV Files", command=select_files)
    btn_select.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
