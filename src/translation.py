from deep_translator import GoogleTranslator

def translate_text(text, source_lang="auto", target_lang="en"):
    try:
        if not text or not text.strip():
            return ""

        translator = GoogleTranslator(
            source=source_lang,
            target=target_lang
        )

        return translator.translate(text)

    except Exception as e:
        print(f"Translation Error: {e}")
        return text