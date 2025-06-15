# Audio to DarkAges MP3 Converter

A Python-based application that allows you to batch convert M4A, WAV, and existing MP3 audio files into a standardized MP3 format (MPEG-2 Layer III settings: 22050 Hz sample rate, 128 kbps bitrate, 16-bit depth). The application features a user-friendly dark-mode GUI using Tkinter with an updated, cleaner look thanks to modern theming, and also supports command-line operations for headless batch processing.

## Features

*   Supports M4A, WAV, and MP3 audio file formats as input.
*   Batch conversion to a specific MP3 format (128 kbps, 22050 Hz).
*   User-friendly dark-mode GUI using Tkinter with an updated, cleaner look thanks to modern theming.
*   Real-time progress tracking and conversion logging within the GUI.
*   Multithreaded GUI operation for a smooth experience without UI freezing during conversion.
*   Command-Line Interface (CLI) for headless batch processing.

## Prerequisites

Before you can run the converter, you'll need the following installed:

*   **Python:** Python 3.9 or higher is recommended (the application has been tested up to Python 3.12). You can download Python from [python.org](https://www.python.org/).
*   **Tkinter:** This is Python's standard GUI library.
    *   For Windows and macOS, Tkinter is usually included with Python.
    *   On Linux, you might need to install it separately using your system's package manager. For example, on Debian/Ubuntu:
        ```bash
        sudo apt-get update
        sudo apt-get install python3-tk
        # Or for a specific Python version like 3.12:
        # sudo apt-get install python3.12-tk
        ```
*   **Pydub:** A Python library for audio manipulation. Install it using pip:
    ```bash
    pip install pydub
    ```
    Alternatively, on some Linux systems (like Debian/Ubuntu), it might be available via the system package manager:
    ```bash
    # sudo apt-get install python3-pydub # (Installs for the system default Python3)
    ```
    Ensure it's installed for the Python version you intend to use (e.g., Python 3.12).
*   **FFmpeg:** Pydub relies on FFmpeg for loading and exporting audio files.
    *   Download FFmpeg binaries from the [official FFmpeg website](https://ffmpeg.org/download.html).
    *   Ensure the `ffmpeg` (and `ffprobe`) executable is in your system's PATH or accessible by the script. On Linux, you can often install it via your package manager:
        ```bash
        sudo apt-get install ffmpeg
        ```

## Installation

1.  **Clone or download the repository:**
    If you have Git installed:
    ```bash
    git clone https://github.com/jinori/darkagesmp3convert.git
    cd darkagesmp3convert
    ```
    Alternatively, you can download the source code as a ZIP file and extract it.

2.  **Install required Python libraries:**
    As mentioned in the prerequisites, ensure `pydub` is installed:
    ```bash
    pip install pydub
    ```
    (Make sure `tkinter` and `FFmpeg` are also set up as described above.)

## Usage

### Graphical User Interface (GUI)

To run the application with its graphical interface:

```bash
python3 Convert.py
# Or, if python3.12 is the specific version you set up:
# python3.12 Convert.py
```

1.  Open the application.
2.  Select the **Input Folder** containing your M4A, WAV, or MP3 files.
3.  Select the **Output Folder** where the converted MP3 files will be saved.
4.  Click **Start Conversion** to begin the process. Progress will be shown in the log and progress bar.

### Command-Line Interface (CLI) for Batch Processing

For advanced users or automated batch processing, you can run the converter from the command line:

```bash
python3 Convert.py --input_folder /path/to/your/audiofiles --output_folder /path/to/save/mp3s
# Example using python3.12:
# python3.12 Convert.py --input_folder ./my_audio --output_folder ./converted_mp3s
```

This mode will process all supported audio files from the input folder and save them to the output folder, printing progress and log messages to the console.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
