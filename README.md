
# SpeechFlow AI
### Multilingual Audio Intelligence

SpeechFlow AI is a Streamlit-based multilingual audio intelligence application designed to transcribe, analyze, translate, and summarize audio recordings.

**Theme:** Charcoal Black | Forest Green | Crimson Red

---

## Features

- Upload WAV, MP3, M4A, FLAC, OGG, MP4, and WEBM audio files.
- Speech-to-text transcription using Faster-Whisper.
- Automatic language detection.
- Support for Tamil, English, Hindi, Malayalam, Telugu, Kannada, and other languages.
- Code-mixed speech support, including Tanglish and Hinglish.
- Optional speaker diarization using pyannote.audio.
- Translation support.
- Conversation statistics and text summarization.
- SQLite session history.
- Downloadable transcripts and analysis reports.
- Custom dark-themed Streamlit interface.

## Technologies Used

- Python
- Streamlit
- Faster-Whisper
- Hugging Face Transformers
- PyTorch
- pyannote.audio
- SQLite
- NLLB Translation Model

## Project Structure

```text
SpeechFlow_AI/
│
├── app.py
├── config.py
├── requirements.txt
├── evaluate.py
├── README.md
├── LICENSE
│
├── components/
│   └── transcript_view.py
│
├── src/
│   ├── audio_processor.py
│   ├── conversation_engine.py
│   ├── database.py
│   ├── emotion_engine.py
│   ├── language_engine.py
│   ├── report_generator.py
│   ├── speaker_engine.py
│   ├── speaker_identity.py
│   ├── speech_engine.py
│   ├── summarizer.py
│   ├── translation.py
│   ├── translation_engine.py
│   └── translator.py
│
└── data/
    ├── database/
    ├── uploads/
    └── reports/
```

## Installation on Windows

### 1. Clone the repository

```bash
git clone https://github.com/aishu042003/SpeechFlow_AI.git
```

### 2. Open the project folder

```bash
cd SpeechFlow_AI
```

### 3. Create a virtual environment

```bash
py -3.11 -m venv .venv
```

### 4. Activate the environment

```bash
.venv\Scripts\activate
```

### 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 6. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open your browser:

http://localhost:8501

## Speaker Diarization Setup

Speaker diarization is optional.

1. Create a Hugging Face account.
2. Generate an access token with read permission.
3. Request access to the required gated pyannote models.
4. Enter your token in the application's speaker diarization section.

Never publish your Hugging Face token or passwords on GitHub.

## System Requirements

- Windows 10 or Windows 11
- Python compatible with project dependencies
- Internet connection for downloading models
- Sufficient RAM for local audio processing
- CPU-based processing support

## Security

- Do not upload API tokens or passwords.
- Keep private configuration files out of GitHub.
- Exclude uploaded audio, databases, and generated private files from public source control.

## Developer

**Project:** SpeechFlow AI

**Category:** Multilingual Audio Intelligence

**Framework:** Streamlit

**Repository:** https://github.com/aishu042003/SpeechFlow_AI

---

*SpeechFlow AI — Making multilingual audio intelligence accessible.*
