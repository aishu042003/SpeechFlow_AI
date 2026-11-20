from pathlib import Path
import soundfile as sf

SUPPORTED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".mpeg",
    ".mpg",
    ".m4a",
    ".flac",
    ".ogg",
    ".mp4",
    ".webm"}

def validate_audio(path):
    audio_path = Path(path)
    if not audio_path.exists():
        return False, "Audio file does not exist."
    if audio_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported audio extension: {audio_path.suffix}"
    if audio_path.stat().st_size == 0:
        return False, "The uploaded file is empty."
    return True, "OK"

def get_audio_info(path):
    try:
        info = sf.info(str(path))
        return {
            "duration_seconds": float(info.duration),
            "sample_rate": int(info.samplerate),
            "channels": int(info.channels),
        }
    except Exception:
        # Compressed audio may not be readable by libsndfile; Whisper can still decode via FFmpeg.
        return {"duration_seconds": 0.0, "sample_rate": 0, "channels": 0}