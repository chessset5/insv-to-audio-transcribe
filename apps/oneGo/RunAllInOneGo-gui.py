#!/usr/bin/env python3

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)


from RunAllInOneGo import run_scripts
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from apps.misc.GlobalVariables import ACCEPTABLE_VIDEO_FILE_TYPES


# Wrapper function to run scripts and show a GUI message
def run_scripts_gui(file_paths: list[str]) -> None:
    # Show the selected files and ask for confirmation
    confirmation = messagebox.askyesno(
        "Confirm Files",
        f"Are you sure you want to run scripts for the following files?\n\n{', '.join(file_paths)}",
    )

    # If the user confirms, run the scripts
    if confirmation:
        # messagebox.showinfo(
        #     "Running Scripts", f"Running scripts for files: {file_paths}"
        # )
        run_scripts(file_paths=file_paths)
        messagebox.showinfo(
            "Finished", f"Finished running scripts for files: {file_paths}"
        )
    else:
        messagebox.showinfo("Cancelled", "Script execution was cancelled.")


# Main application class
class INSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video File Transcriber")
        self.root.geometry("600x400")

        # List to store file paths and their associated checkboxes
        self.file_paths = []
        self.checkboxes = []

        # Top buttons
        self.select_button = tk.Button(
            root, text="Select Video files", command=self.select_files
        )
        self.select_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.toggle_all_button = tk.Button(
            root, text="Toggle all", command=self.toggle_all
        )
        self.toggle_all_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Text box with scrollbars
        self.text_box_frame = tk.Frame(root)
        self.text_box_frame.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        # Canvas and scrollbars
        self.canvas = tk.Canvas(self.text_box_frame, bg="white")
        self.h_scrollbar = ttk.Scrollbar(
            self.text_box_frame, orient="horizontal", command=self.canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            self.text_box_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(
            self.canvas, bg="white"
        )  # Set background to white

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(
            xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set
        )

        # Pack scrollbars and canvas
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel events to the canvas for both horizontal and vertical scrolling
        self.canvas.bind_all(
            "<MouseWheel>", self.on_mouse_wheel
        )  # Vertical scrolling (Windows/macOS)
        self.canvas.bind_all(
            "<Shift-MouseWheel>", self.on_horizontal_mouse_wheel
        )  # Horizontal scrolling (Windows/macOS)
        self.canvas.bind_all(
            "<Button-4>", self.on_mouse_wheel
        )  # Vertical scrolling (Linux, up)
        self.canvas.bind_all(
            "<Button-5>", self.on_mouse_wheel
        )  # Vertical scrolling (Linux, down)
        self.canvas.bind_all(
            "<Shift-Button-4>", self.on_horizontal_mouse_wheel
        )  # Horizontal scrolling (Linux, left)
        self.canvas.bind_all(
            "<Shift-Button-5>", self.on_horizontal_mouse_wheel
        )  # Horizontal scrolling (Linux, right)

        # Bottom buttons
        self.remove_button = tk.Button(root, text="Remove", command=self.remove_files)
        self.remove_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.run_button = tk.Button(root, text="Run all", command=self.run_all)
        self.run_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Configure grid weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def select_files(self):
        # Open file dialog to select .insv files
        filetypes = ACCEPTABLE_VIDEO_FILE_TYPES
        selected_files = filedialog.askopenfilenames(
            title="Select Video files", filetypes=filetypes
        )

        # Add selected files to the list and update the text box
        for file_path in selected_files:
            if file_path not in self.file_paths:
                self.file_paths.append(file_path)
                self.add_file_to_text_box(file_path)

    def add_file_to_text_box(self, file_path):
        # Create a checkbox and label for the file path
        var = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(
            self.scrollable_frame, variable=var, bg="white"
        )  # Set background to white
        label = tk.Label(
            self.scrollable_frame, text=file_path, anchor="w", bg="white"
        )  # Set background to white

        # Store the checkbox and its variable
        self.checkboxes.append((var, checkbox, label))

        # Add to the scrollable frame
        checkbox.grid(row=len(self.checkboxes) - 1, column=0, sticky="w")
        label.grid(row=len(self.checkboxes) - 1, column=1, sticky="w")

    def toggle_all(self):
        # Toggle all checkboxes
        if not self.checkboxes:
            return

        # Determine the new state based on the first checkbox
        new_state = not self.checkboxes[0][0].get()

        for var, checkbox, label in self.checkboxes:
            var.set(new_state)

    def remove_files(self):
        # Remove all checked files
        remaining_files = []
        remaining_checkboxes = []

        for i, (var, checkbox, label) in enumerate(self.checkboxes):
            if not var.get():
                remaining_files.append(self.file_paths[i])
                remaining_checkboxes.append((var, checkbox, label))

        # Update the file paths and checkboxes
        self.file_paths = remaining_files
        self.checkboxes = remaining_checkboxes

        # Clear the scrollable frame and re-add the remaining files
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for var, checkbox, label in self.checkboxes:
            checkbox.grid(row=len(self.checkboxes), column=0, sticky="w")
            label.grid(row=len(self.checkboxes), column=1, sticky="w")

    def run_all(self):
        # Get the selected file paths and pass them to the run_scripts_gui function
        selected_files = [
            self.file_paths[i]
            for i, (var, _, _) in enumerate(self.checkboxes)
            if var.get()
        ]
        if selected_files:
            run_scripts_gui(selected_files)
        else:
            messagebox.showwarning(
                "No Files Selected", "Please select at least one file to run."
            )

    def on_mouse_wheel(self, event):
        # Handle vertical scrolling
        if event.delta:  # Windows and macOS
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num == 4:  # Linux (up)
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux (down)
            self.canvas.yview_scroll(1, "units")

    def on_horizontal_mouse_wheel(self, event):
        # Handle horizontal scrolling
        if event.delta:  # Windows and macOS
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")
        elif event.num == 4:  # Linux (left)
            self.canvas.xview_scroll(-1, "units")
        elif event.num == 5:  # Linux (right)
            self.canvas.xview_scroll(1, "units")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = INSVApp(root)
    root.mainloop()
