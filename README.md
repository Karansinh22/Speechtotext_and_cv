<div align="center">

# 🎧 Speech & Vision Toolkit

**Real-time OCR reading with voice output, paired with a bidirectional speech-to-text / text-to-speech web app.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract_OCR-4E9A06?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Edge TTS](https://img.shields.io/badge/edge--tts-0078D4?style=flat-square)

</div>

---

## Overview

Two complementary modules that together let a machine **read what it sees** and **speak and listen** to a person:

| Module | What it does |
|---|---|
| **`Computer vision/`** | Captures a live webcam feed, detects text with **Tesseract OCR**, reads it aloud, and raises visual + audio alerts when a target word appears. Every detection is timestamped to CSV. |
| **`Speechtotextandviceversa/`** | A Flask web app for **speech-to-text** (browser Web Speech API) and **text-to-speech** (`edge-tts` neural voices), with standalone Python scripts for each direction. |

---

## Features

**Computer vision — live text reader**
- Real-time text detection from a camera feed
- Spoken output of detected text
- Target-word detection with on-screen and audible alerts
- CSV logging of every detection with timestamps
- Tunable preprocessing for better OCR accuracy
- Cross-platform (Windows, macOS, Linux)

**Speech module**
- Live microphone → text transcription in the browser
- Natural neural text-to-speech via `edge-tts`
- Copy-to-clipboard transcripts
- Standalone `SpeechToText.py` / `TextToSpeech.py` scripts for scripted use

---

## Quick Start

### Prerequisites
- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and on `PATH`
- A working webcam and microphone

```bash
# Linux
sudo apt update && sudo apt install tesseract-ocr libtesseract-dev

# macOS
brew install tesseract
```

### Run the live text reader

```bash
cd "Computer vision"
pip install opencv-python pytesseract pyttsx3 pillow
python cv_text_reader.py
```

### Run the speech web app

```bash
cd Speechtotextandviceversa
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

---

## Repository Layout

```
.
├── Computer vision/              # Live OCR + speech output
│   ├── cv_text_reader.py         # Main real-time detection loop
│   ├── check_tesseract.py        # Verifies the Tesseract install
│   ├── test_ocr.py               # OCR sanity check on a still image
│   └── text_detection_log.csv    # Timestamped detection log
│
└── Speechtotextandviceversa/     # Speech web app
    ├── app.py                    # Flask server
    ├── SpeechToText.py           # Standalone STT script
    ├── TextToSpeech.py           # Standalone TTS script
    └── requirements.txt
```

---

## Tech Stack

`Python` · `OpenCV` · `Tesseract OCR` · `pytesseract` · `Flask` · `edge-tts` · `pygame` · `Web Speech API`

---

<div align="center">

Built by **[Karansinh Desai](https://github.com/Karansinh22)** · [LinkedIn](https://www.linkedin.com/in/karansinh-desai-024144284)

</div>
