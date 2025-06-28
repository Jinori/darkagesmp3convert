import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from pydub import AudioSegment
from threading import Thread

# Function to convert audio to MP3 with MPEG-2 Layer III settings
def convert_to_mp3(file_path, output_path, bitrate="128k", sample_rate=22050, bit_depth=16):
    try:
        # Load audio file using pydub's AudioSegment
        audio = AudioSegment.from_file(file_path)
        
        # Ensure audio is in 16-bit depth
        audio = audio.set_sample_width(bit_depth // 8)  # 16 bits = 2 bytes
        
        # Ensure audio is in the correct sample rate for MPEG-2 Layer III
        audio = audio.set_frame_rate(sample_rate)
        
        # Export the file as MP3 using the appropriate settings
        audio.export(output_path, format="mp3", bitrate=bitrate, parameters=["-ar", str(sample_rate), "-acodec", "libmp3lame", "-write_xing", "0"])
        return f"Converted {file_path} to {output_path}\n"
    except Exception as e:
        return f"Failed to convert {file_path}: {str(e)}\n"

# Function to count the total number of files to convert
def count_files(input_folder):
    total_files = 0
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(('.m4a', '.wav', '.mp3')):
                total_files += 1
    return total_files

# Function to batch convert M4A, WAV, and MP3 files to MP3
def batch_convert_audio_to_mp3(input_folder, output_folder, log_widget, progress, total_files, bitrate="128k", sample_rate=22050, bit_depth=16):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    log_widget.insert(tk.END, "Starting conversion...\n")
    
    converted_files = 0
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            # Check for M4A, WAV, or MP3 files
            if file_name.endswith(('.m4a', '.wav', '.mp3')):
                file_path = os.path.join(root, file_name)
                output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".mp3")
                
                # Convert the file to MP3 (re-encoding MP3 files as well)
                result = convert_to_mp3(file_path, output_file, bitrate=bitrate, sample_rate=sample_rate, bit_depth=bit_depth)
                log_widget.insert(tk.END, result)
                log_widget.see(tk.END)
                
                # Update progress bar
                converted_files += 1
                progress['value'] = (converted_files / total_files) * 100
                log_widget.update_idletasks()
                
    log_widget.insert(tk.END, "Conversion finished!\n")

# Function to run conversion in a separate thread to avoid blocking the UI
def start_conversion(input_folder, output_folder, log_widget, progress):
    total_files = count_files(input_folder)
    if total_files > 0:
        progress['value'] = 0
        thread = Thread(target=batch_convert_audio_to_mp3, args=(input_folder, output_folder, log_widget, progress, total_files))
        thread.start()
    else:
        log_widget.insert(tk.END, "No valid files found for conversion.\n")

# GUI with dark mode and progress bar
def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("MP3/M4A/Wav to DarkAges MP3 Converter")
    root.geometry("600x450")
    
    # Set dark mode colors
    bg_color = "#2b2b2b"
    fg_color = "#ffffff"
    button_color = "#5a5a5a"
    root.configure(bg=bg_color)
    
    # Variables to store folder paths
    input_folder = tk.StringVar()
    output_folder = tk.StringVar()

    # Input folder selection
    def select_input_folder():
        folder = filedialog.askdirectory()
        if folder:
            input_folder.set(folder)

    # Output folder selection
    def select_output_folder():
        folder = filedialog.askdirectory()
        if folder:
            output_folder.set(folder)

    # Labels and buttons
    tk.Label(root, text="Input Folder:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=input_folder, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_input_folder, bg=button_color, fg=fg_color).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Output Folder:", bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_folder, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_output_folder, bg=button_color, fg=fg_color).grid(row=1, column=2, padx=10, pady=10)

    # Conversion log
    log_label = tk.Label(root, text="Conversion Log:", bg=bg_color, fg=fg_color)
    log_label.grid(row=2, column=0, padx=10, pady=10)
    
    log_widget = scrolledtext.ScrolledText(root, width=70, height=10, bg=bg_color, fg=fg_color, insertbackground=fg_color)
    log_widget.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Progress bar
    progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Start conversion button
    def on_convert():
        if input_folder.get() and output_folder.get():
            log_widget.delete(1.0, tk.END)  # Clear log
            start_conversion(input_folder.get(), output_folder.get(), log_widget, progress)

    convert_button = tk.Button(root, text="Start Conversion", command=on_convert, bg=button_color, fg=fg_color)
    convert_button.grid(row=5, column=1, pady=20)

    root.mainloop()

# Run the GUI
create_gui()
