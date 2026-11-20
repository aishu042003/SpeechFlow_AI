
import re
import torch
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==========================================
# MODEL CONFIGURATION
# ==========================================

MODEL_NAME = "facebook/nllb-200-distilled-600M"


# ==========================================
# SUPPORTED LANGUAGES
# ==========================================

LANGUAGES = {
    "Arabic": "arb_Arab",
    "Bengali": "ben_Beng",
    "Chinese (Simplified)": "zho_Hans",
    "English": "eng_Latn",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva",
    "Indonesian": "ind_Latn",
    "Italian": "ita_Latn",
    "Japanese": "jpn_Jpan",
    "Kannada": "kan_Knda",
    "Korean": "kor_Hang",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Nepali": "npi_Deva",
    "Portuguese": "por_Latn",
    "Punjabi": "pan_Guru",
    "Russian": "rus_Cyrl",
    "Spanish": "spa_Latn",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Thai": "tha_Thai",
    "Turkish": "tur_Latn",
    "Urdu": "urd_Arab",
    "Vietnamese": "vie_Latn",
}


ALIASES = {
    "ta": "Tamil",
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "ar": "Arabic",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ja": "Japanese",
    "ko": "Korean",
}


# ==========================================
# LOAD TRANSLATION MODEL
# ==========================================

@lru_cache(maxsize=1)
def load_translation_model():

    print("Loading Hugging Face translation model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    model.eval()

    print("Translation model ready!")

    return tokenizer, model


# ==========================================
# GET SUPPORTED LANGUAGES
# ==========================================

def get_supported_languages():

    return LANGUAGES.copy()


# ==========================================
# RESOLVE LANGUAGE
# ==========================================

def resolve_language(language):

    if not language:
        return None

    language = str(language).strip()

    if language.lower() == "auto":
        return "auto"

    if language.lower() == "tanglish":
        return "Tanglish"

    if language in LANGUAGES:
        return language

    alias = ALIASES.get(language.lower())

    if alias:
        return alias

    for name in LANGUAGES:

        if name.lower() == language.lower():
            return name

    return None


# ==========================================
# AUTOMATIC LANGUAGE DETECTION
# ==========================================

def detect_source_language(text):

    patterns = [
        (r"[\u0B80-\u0BFF]", "Tamil"),
        (r"[\u0C00-\u0C7F]", "Telugu"),
        (r"[\u0D00-\u0D7F]", "Malayalam"),
        (r"[\u0C80-\u0CFF]", "Kannada"),
        (r"[\u0900-\u097F]", "Hindi"),
        (r"[\u0980-\u09FF]", "Bengali"),
        (r"[\u0A00-\u0A7F]", "Punjabi"),
        (r"[\u0A80-\u0AFF]", "Gujarati"),
        (r"[\u0600-\u06FF]", "Arabic"),
        (r"[\u0400-\u04FF]", "Russian"),
    ]

    for pattern, language in patterns:

        if re.search(pattern, text):
            return language

    return "English"


# ==========================================
# SPLIT LONG TEXT
# ==========================================

def split_text(text, max_chars=350):

    sentences = re.split(r"(?<=[.!?।])\s+", text.strip())

    chunks = []
    current = ""

    for sentence in sentences:

        if len(current) + len(sentence) <= max_chars:

            current = (current + " " + sentence).strip()

        else:

            if current:
                chunks.append(current)

            if len(sentence) > max_chars:

                for i in range(0, len(sentence), max_chars):
                    chunks.append(sentence[i:i + max_chars])

                current = ""

            else:
                current = sentence

    if current:
        chunks.append(current)

    return chunks


# ==========================================
# TAMIL TO NATURAL-STYLE TANGLISH
# ==========================================

def convert_tamil_to_tanglish(text):

    vowels = {
        "அ": "a",
        "ஆ": "aa",
        "இ": "i",
        "ஈ": "ee",
        "உ": "u",
        "ஊ": "oo",
        "எ": "e",
        "ஏ": "ee",
        "ஐ": "ai",
        "ஒ": "o",
        "ஓ": "oo",
        "ஔ": "au",
    }

    consonants = {
        "க": "k",
        "ங": "ng",
        "ச": "s",
        "ஞ": "nj",
        "ட": "d",
        "ண": "n",
        "த": "th",
        "ந": "n",
        "ப": "p",
        "ம": "m",
        "ய": "y",
        "ர": "r",
        "ல": "l",
        "வ": "v",
        "ழ": "zh",
        "ள": "l",
        "ற": "r",
        "ன": "n",
        "ஜ": "j",
        "ஷ": "sh",
        "ஸ": "s",
        "ஹ": "h",
        "ஶ": "sh",
    }

    vowel_signs = {
        "ா": "aa",
        "ி": "i",
        "ீ": "ee",
        "ு": "u",
        "ூ": "oo",
        "ெ": "e",
        "ே": "ee",
        "ை": "ai",
        "ொ": "o",
        "ோ": "oo",
        "ௌ": "au",
    }

    pulli = "்"

    result = []
    i = 0

    while i < len(text):

        char = text[i]

        # Independent vowels
        if char in vowels:

            result.append(vowels[char])
            i += 1
            continue

        # Special Tamil ending: கள் -> gal
        if (
            char == "க"
            and i + 2 < len(text)
            and text[i + 1] == "ள"
            and text[i + 2] == pulli
        ):

            result.append("gal")
            i += 3
            continue

        # Tamil consonants
        if char in consonants:

            sound = consonants[char]

            if i + 1 < len(text):

                next_char = text[i + 1]

                # Consonant with pulli
                if next_char == pulli:

                    result.append(sound)
                    i += 2
                    continue

                # Consonant with vowel sign
                if next_char in vowel_signs:

                    result.append(sound + vowel_signs[next_char])
                    i += 2
                    continue

            # Default Tamil vowel
            result.append(sound + "a")
            i += 1
            continue

        # Keep spaces, punctuation and other characters
        result.append(char)
        i += 1

    output = "".join(result)

    # Capitalize the first letter
    output = output[:1].upper() + output[1:]

    return output


# ==========================================
# TRANSLATE ONE CHUNK
# ==========================================

def translate_chunk(
    text,
    source_code,
    target_code,
    tokenizer,
    model
):

    tokenizer.src_lang = source_code

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    target_id = tokenizer.convert_tokens_to_ids(target_code)

    with torch.no_grad():

        output = model.generate(
            **inputs,
            forced_bos_token_id=target_id,
            max_length=512,
            num_beams=2
        )

    translated = tokenizer.batch_decode(
        output,
        skip_special_tokens=True
    )[0]

    return translated


# ==========================================
# MAIN TRANSLATION FUNCTION
# ==========================================

def translate_text(
    text,
    target_language="English",
    source_language="auto"
):

    if not text or not text.strip():
        return ""

    try:

        target = resolve_language(target_language)

        if target is None:
            return f"Unsupported target language: {target_language}"

        source = resolve_language(source_language)

        if source is None:
            return f"Unsupported source language: {source_language}"

        # Detect source language automatically
        if source == "auto":

            source = detect_source_language(text)

        # Tanglish uses Tamil as intermediate language
        if target == "Tanglish":

            target_name = "Tamil"

        else:

            target_name = target

        source_code = LANGUAGES[source]
        target_code = LANGUAGES[target_name]

        # No translation needed
        if source_code == target_code:

            translated = text

        else:

            tokenizer, model = load_translation_model()

            chunks = split_text(text)

            translated_chunks = []

            for chunk in chunks:

                translated_chunk_text = translate_chunk(
                    chunk,
                    source_code,
                    target_code,
                    tokenizer,
                    model
                )

                translated_chunks.append(
                    translated_chunk_text
                )

            translated = " ".join(translated_chunks)

        # Convert Tamil to Tanglish
        if target == "Tanglish":

            return convert_tamil_to_tanglish(translated)

        return translated

    except Exception as error:

        return f"Translation failed: {error}"
