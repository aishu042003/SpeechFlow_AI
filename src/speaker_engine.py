
"""
SpeechFlow AI - Speaker Diarization Engine

Features:
- Speaker identification
- Speaker start and end timestamps
- CPU processing
- Cached model loading
"""

import os

# Low-memory CPU settings
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from pathlib import Path
from functools import lru_cache


# ==========================================
# LOAD SPEAKER DIARIZATION MODEL
# ==========================================

@lru_cache(maxsize=1)
def load_diarization_pipeline(hf_token):

    from pyannote.audio import Pipeline

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token
    )

    if pipeline is None:
        raise RuntimeError(
            "Unable to load speaker diarization model."
        )

    pipeline.to("cpu")

    return pipeline


# ==========================================
# IDENTIFY SPEAKERS
# ==========================================

def diarize_audio(audio_path, hf_token):

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    if audio_path.stat().st_size == 0:
        raise ValueError("Audio file is empty.")

    if not hf_token or not hf_token.strip():
        raise ValueError(
            "Please enter your Hugging Face token."
        )

    # Load model
    pipeline = load_diarization_pipeline(
        hf_token.strip()
    )

    # Run speaker identification
    result = pipeline(str(audio_path))

    # Extract annotation
    annotation = getattr(
        result,
        "speaker_diarization",
        result
    )

    speaker_rows = []

    for turn, _, speaker in annotation.itertracks(
        yield_label=True
    ):

        speaker_rows.append({
            "start": round(float(turn.start), 2),
            "end": round(float(turn.end), 2),
            "speaker": str(speaker)
        })

    if not speaker_rows:
        raise ValueError(
            "No speakers detected in this audio."
        )

    return speaker_rows
