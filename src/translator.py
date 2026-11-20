def translate_text(text, target_language):
    if not text.strip():
        return ""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=target_language).translate(text)
    except Exception as exc:
        raise RuntimeError(
            f"Translation failed. Check your internet connection and target language: {exc}"
        ) from exc