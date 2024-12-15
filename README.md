# MP3/M4A/WAV to DarkAges MP3 Converter

A Python-based GUI application that allows you to batch convert M4A, WAV, and MP3 audio files into MP3 format optimized for MPEG-2 Layer III settings. The application features a dark-mode interface with a progress bar and conversion log.

## Features

Supports M4A, WAV, and MP3 audio file formats. 

Batch conversion to MP3 with custom bitrate, sample rate, and bit depth. 

Real-time progress tracking and logging. 

User-friendly dark-mode GUI using Tkinter.

Multithreaded for smooth operation without UI freezing.


# Installation 

Follow these steps to install and run the converter:

### Prerequisites

Python 3.8 or higher Download and install Python from python.org. 

##### Required Python libraries 

Install the required dependencies using pip: 

```pip install pydub tkinter``` 

##### FFmpeg 

The application relies on FFmpeg for audio processing.

Download FFmpeg binaries from the official website. 

Add FFmpeg to your system's PATH.

# Download and Clone the repository:

```git clone https://github.com/yourusername/audio-converter.git cd audio-converter``` 

Run the script:

````python converter.py````

# Usage 

Open the application. 

Select the Input Folder containing your M4A/WAV/MP3 files. 

Select the Output Folder to save the converted MP3 files. 

Click Start Conversion to begin.

## License

[MIT](https://choosealicense.com/licenses/mit/)
