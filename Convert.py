import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from pydub import AudioSegment
from threading import Thread
import argparse # Added for CLI arguments

# Function to convert audio to MP3 with MPEG-2 Layer III settings
def convert_to_mp3(file_path, output_path, bitrate="128k", sample_rate=22050, bit_depth=16):
    try:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_sample_width(bit_depth // 8)
        audio = audio.set_frame_rate(sample_rate)
        audio.export(output_path, format="mp3", bitrate=bitrate, parameters=["-ar", str(sample_rate), "-acodec", "libmp3lame"])
        return f"Converted {file_path} to {output_path}\n"
    except Exception as e:
        return f"Failed to convert {file_path}: {str(e)}\n"

# Function to count the total number of files to convert
def count_files(input_folder):
    total_files = 0
    for root_dir, _, files_in_dir in os.walk(input_folder):
        for file_name in files_in_dir:
            if file_name.lower().endswith(('.m4a', '.wav', '.mp3')):
                total_files += 1
    return total_files

# Function to batch convert M4A, WAV, and MP3 files to MP3
def batch_convert_audio_to_mp3(input_folder, output_folder, log_widget, progress, total_files, bitrate="128k", sample_rate=22050, bit_depth=16):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ensure log_widget has an 'insert' method and progress has a 'update_value' method or can be dictionary
    log_widget_insert = getattr(log_widget, "insert", lambda pos, msg: print(msg, end=''))
    log_widget_see = getattr(log_widget, "see", lambda pos: None)
    log_widget_update_idletasks = getattr(log_widget, "update_idletasks", lambda: None)

    def progress_update(val):
        if isinstance(progress, dict):
            progress['value'] = val
        elif hasattr(progress, 'update_value'):
            progress.update_value(val)
        else: # Simple print for CLI progress
            print(f"Progress: {val:.2f}%")

    log_widget_insert(tk.END if hasattr(tk, "END") else "end", "Starting conversion...\n") # Use string "end" if tk.END not available (e.g. CLI)

    converted_files = 0
    for root_dir, _, files_in_dir in os.walk(input_folder):
        for file_name in files_in_dir:
            if file_name.lower().endswith(('.m4a', '.wav', '.mp3')):
                file_path = os.path.join(root_dir, file_name)
                output_file_name = os.path.splitext(file_name)[0] + ".mp3"
                output_path_full = os.path.join(output_folder, output_file_name)

                result = convert_to_mp3(file_path, output_path_full, bitrate=bitrate, sample_rate=sample_rate, bit_depth=bit_depth)
                log_widget_insert(tk.END if hasattr(tk, "END") else "end", result)
                log_widget_see(tk.END if hasattr(tk, "END") else "end")

                converted_files += 1
                progress_val = (converted_files / total_files) * 100 if total_files > 0 else 0
                progress_update(progress_val)
                log_widget_update_idletasks()

    log_widget_insert(tk.END if hasattr(tk, "END") else "end", "Conversion finished!\n")

# Function to run conversion in a separate thread to avoid blocking the UI (for GUI mode)
def start_conversion_thread(input_folder, output_folder, log_widget, progress):
    total_files = count_files(input_folder)
    if total_files > 0:
        if isinstance(progress, dict): progress['value'] = 0
        elif hasattr(progress, 'update_value'): progress.update_value(0)

        thread = Thread(target=batch_convert_audio_to_mp3, args=(input_folder, output_folder, log_widget, progress, total_files), daemon=True)
        thread.start()
    else:
        log_insert_method = getattr(log_widget, "insert", lambda pos, msg: print(msg, end=''))
        log_insert_method(tk.END if hasattr(tk, "END") else "end", "No valid audio files found for conversion.\n")

# --- Mock Objects for CLI Mode ---
class MockLogger:
    def insert(self, position, message): # position can be tk.END or string "end"
        print(message, end='') # Print message, no new line if message already has one
    def see(self, position):
        pass # No-op for CLI
    def update_idletasks(self):
        pass # No-op for CLI
    def delete(self, start, end): # Added to match GUI log_widget clear
        print("--- Log cleared ---")

class MockProgress:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        print(f"Progress: {self._value:.2f}%")

    # Keep dictionary-like access for compatibility if batch_convert_audio_to_mp3 uses it
    def __setitem__(self, key, val):
        if key == 'value':
            self.value = val
        else:
            raise KeyError(f"MockProgress only supports 'value' key, not {key}")

    def __getitem__(self, key):
        if key == 'value':
            return self._value
        raise KeyError(f"MockProgress only supports 'value' key, not {key}")


# --- GUI ---
def create_gui():
    root = tk.Tk()
    root.title("Audio to DarkAges MP3 Converter")
    root.geometry("650x500")

    bg_color = "#2b2b2b"
    fg_color = "#ffffff"
    entry_bg_color = "#3c3f41"
    button_bg_color = "#5a5a5a"
    button_fg_color = "#ffffff"
    active_button_bg_color = "#6a6a6a"

    style = ttk.Style(root)
    style.theme_use('clam')

    style.configure('.', background=bg_color, foreground=fg_color)
    style.configure('TEntry', fieldbackground=entry_bg_color, foreground=fg_color, insertcolor=fg_color)
    style.configure('TButton', background=button_bg_color, foreground=button_fg_color, padding=5)
    style.map('TButton',
              background=[('active', active_button_bg_color), ('disabled', '#4a4a4a')],
              foreground=[('active', button_fg_color), ('disabled', '#aaaaaa')])
    style.configure('TLabel', background=bg_color, foreground=fg_color, padding=5)
    style.configure('Horizontal.TProgressbar', background=button_bg_color, troughcolor=bg_color)
    root.configure(bg=bg_color)

    input_folder = tk.StringVar()
    output_folder = tk.StringVar()

    def select_input_folder():
        folder = filedialog.askdirectory()
        if folder:
            input_folder.set(folder)

    def select_output_folder():
        folder = filedialog.askdirectory()
        if folder:
            output_folder.set(folder)

    ttk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Entry(root, textvariable=input_folder, width=60).grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=10)

    ttk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Entry(root, textvariable=output_folder, width=60).grid(row=1, column=1, padx=10, pady=10)
    ttk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    ttk.Label(root, text="Conversion Log:").grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
    log_widget = scrolledtext.ScrolledText(root, width=80, height=15,
                                           bg=entry_bg_color, fg=fg_color,
                                           insertbackground=fg_color,
                                           relief=tk.FLAT, borderwidth=1)
    log_widget.grid(row=3, column=0, columnspan=3, padx=10, pady=(0,10))

    progress = ttk.Progressbar(root, orient="horizontal", length=580, mode="determinate")
    progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def on_convert():
        in_folder = input_folder.get()
        out_folder = output_folder.get()
        if in_folder and out_folder:
            log_widget.delete(1.0, tk.END)
            start_conversion_thread(in_folder, out_folder, log_widget, progress)
        else:
            log_widget.insert(tk.END, "Please select both input and output folders.\n")

    convert_button = ttk.Button(root, text="Start Conversion", command=on_convert)
    convert_button.grid(row=5, column=0, columnspan=3, pady=20)
    root.grid_columnconfigure(1, weight=1)
    root.mainloop()

# Main execution: CLI or GUI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio to MP3 Converter")
    parser.add_argument("--input_folder", type=str, help="Path to the input folder for batch conversion.")
    parser.add_argument("--output_folder", type=str, help="Path to the output folder for batch conversion.")
    args = parser.parse_args()

    if args.input_folder and args.output_folder:
        print("Running in CLI mode.")
        mock_logger = MockLogger()
        mock_progress = MockProgress() # Use the class that prints progress

        total_files = count_files(args.input_folder)
        if total_files > 0:
            # Call batch_convert_audio_to_mp3 directly for CLI mode (no separate thread)
            batch_convert_audio_to_mp3(args.input_folder, args.output_folder, mock_logger, mock_progress, total_files)
        else:
            mock_logger.insert("end", "No valid audio files found for conversion.\n")
    else:
        print("Running in GUI mode.")
        create_gui()
