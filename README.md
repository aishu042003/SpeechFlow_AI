# SpeechFlow AI

SpeechFlow AI is a Streamlit starter app for audio transcription and basic speech analytics, styled with Charcoal Black, Forest Green and Crimson Red.

## Features
- Upload WAV, MP3, M4A, FLAC, OGG, MP4 and WEBM audio
- Speech-to-text using Faster-Whisper
- Language identification
- Optional speaker diarization using pyannote.audio
- Conversation statistics and extractive summary
- Optional translation using deep-translator
- SQLite session history
- Downloadable transcript and analysis report
- Dark neon Streamlit interface

## Windows installation

Open Command Prompt or the VS Code terminal in this folder:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py