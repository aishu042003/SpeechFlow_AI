def detect_language(text, whisper_language=None):
    if whisper_language:
        return whisper_language
    if not text.strip():
        return "unknown"
    try:
        from langdetect import detect
        return detect(text)
    except Exception:
        return "unknown"