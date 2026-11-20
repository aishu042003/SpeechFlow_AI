
"""
SpeechFlow AI - Multilingual Speech Engine

Features:
- Automatic language detection
- Multilingual transcription
- Tamil, English, Hindi, Malayalam, Telugu, Kannada and more
- Code-mixed speech support (Tanglish, Hinglish, etc.)
- CPU and low-memory optimization
"""

import os

# ==========================================
# LOW MEMORY SETTINGS
# ==========================================

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel


# ==========================================
# SUPPORTED LANGUAGES
# ==========================================

SUPPORTED_LANGUAGES = {
    "Tamil": "ta",
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
}


# ==========================================
# LOAD WHISPER MODEL
# ==========================================

@lru_cache(maxsize=1)
def load_model(model_size="tiny"):

    return WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
        cpu_threads=2,
        num_workers=1
    )


# ==========================================
# LANGUAGE PROMPT
# ==========================================

def build_language_prompt(selected_languages=None):

    if not selected_languages:
        return None

    language_names = []

    for item in selected_languages:

        if item in SUPPORTED_LANGUAGES:
            language_names.append(item)

        elif item in SUPPORTED_LANGUAGES.values():

            for name, code in SUPPORTED_LANGUAGES.items():

                if code == item:
                    language_names.append(name)
                    break

    language_names = list(dict.fromkeys(language_names))

    if not language_names:
        return None

    return (
        "This audio may contain multiple languages, including "
        + ", ".join(language_names)
        + ". Preserve the original spoken words. "
        "The conversation may switch between languages. "
        "Do not translate the speech."
    )


# ==========================================
# TRANSCRIBE AUDIO
# ==========================================

def transcribe_audio(
    audio_path,
    model_size="tiny",
    language=None,
    selected_languages=None
):

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    if audio_path.stat().st_size == 0:
        raise ValueError("The uploaded audio file is empty.")

    if language and language not in SUPPORTED_LANGUAGES.values():
        raise ValueError(
            f"Unsupported language code: {language}"
        )

    model = load_model(model_size)

    prompt = build_language_prompt(selected_languages)

    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        beam_size=1,
        best_of=1,
        vad_filter=True,
        condition_on_previous_text=False,
        initial_prompt=prompt
    )

    segment_list = []
    text_parts = []

    for segment in segments:

        segment_text = segment.text.strip()

        if not segment_text:
            continue

        text_parts.append(segment_text)

        segment_list.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment_text
        })

    full_text = " ".join(text_parts).strip()

    if not full_text:
        raise ValueError(
            "No speech was detected. Please try another audio file."
        )

    return {
        "text": full_text,
        "segments": segment_list,
        "language": info.language,
        "language_probability": info.language_probability
    }
