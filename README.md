# Summarizerly - How to Run

## Prerequisites

Before running the python code, you need two external tools installed on your Windows system:

1.  **Tesseract OCR** (For Image Text Extraction)
    -   Download from: [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    -   Install it (e.g., to `C:\Program Files\Tesseract-OCR`)
    -   **Important**: Add `C:\Program Files\Tesseract-OCR` to your System PATH environment variable.

2.  **FFmpeg** (For Audio/Video Processing)
    -   Download from: [ffmpeg.org](https://ffmpeg.org/download.html) (Get a Windows build, like from gyan.dev)
    -   Extract the zip file.
    -   Add the `bin` folder (where `ffmpeg.exe` is) to your System PATH environment variable.

## Step 1: Install Python Dependencies

Open your terminal (PowerShell or Command Prompt) in this directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

Run the Streamlit app with:

```bash
streamlit run app.py
```

This will open a new tab in your web browser with the Summarizerly interface.

## Usage

1.  Click "Browse files" to upload a PDF, Image, or Audio/Video file.
2.  Wait for the system to process and extract text.
3.  Click the "Summarize" button to generate the summary.

*Note: The first time you run a summarization or audio transcription, the models (T5-small and Whisper) will be downloaded. This might take a few minutes depending on your internet speed.*
