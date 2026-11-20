
import streamlit as st
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

from config import APP_TITLE, UPLOAD_DIR

# ==========================================
# COMPONENT IMPORTS
# ==========================================

from components.dashboard import show_dashboard
from components.transcript_view import show_transcript
from components.analytics import show_analytics
from components.theme import apply_custom_theme

# ==========================================
# CORE MODULE IMPORTS
# ==========================================

from src.audio_processor import validate_audio, get_audio_info
from src.speech_engine import transcribe_audio, SUPPORTED_LANGUAGES
from src.language_engine import detect_language
from src.conversation_engine import analyze_conversation
from src.emotion_engine import analyze_emotion
from src.summarizer import summarize_text
from src.translation_engine import translate_text, get_supported_languages
from src.report_generator import create_report
from src.database import init_db, save_session

# ==========================================
# OPTIONAL SPEAKER MODULES
# ==========================================

try:
    from src.speaker_engine import diarize_audio
    from src.speaker_identity import assign_speaker_labels
    SPEAKER_AVAILABLE = True
except ImportError:
    SPEAKER_AVAILABLE = False

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INITIALIZE APPLICATION
# ==========================================

apply_custom_theme()
init_db()

# ==========================================
# TRANSCRIPTION LANGUAGES
# ==========================================

LANGUAGE_CODES = {
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
    "Russian": "ru"
}

LANGUAGE_NAMES = list(LANGUAGE_CODES.keys())

# ==========================================
# TRANSLATION LANGUAGES
# ==========================================

FALLBACK_TRANSLATION_LANGUAGES = {
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Odia": "or",
    "Persian": "fa",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Russian": "ru",
    "Spanish": "es",
    "Swahili": "sw",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Urdu": "ur",
    "Vietnamese": "vi"
}

try:
    TRANSLATION_LANGUAGE_MAP = get_supported_languages()

    if not TRANSLATION_LANGUAGE_MAP:
        TRANSLATION_LANGUAGE_MAP = (
            FALLBACK_TRANSLATION_LANGUAGES.copy()
        )

except Exception:
    TRANSLATION_LANGUAGE_MAP = (
        FALLBACK_TRANSLATION_LANGUAGES.copy()
    )

TRANSLATION_OPTIONS = (
    ["None", "Tanglish"]
    + sorted(
        TRANSLATION_LANGUAGE_MAP.keys(),
        key=str.lower
    )
)

TRANSLATION_LIST_IS_FALLBACK = (
    TRANSLATION_LANGUAGE_MAP
    == FALLBACK_TRANSLATION_LANGUAGES
)

# ==========================================
# DASHBOARD
# ==========================================

show_dashboard()

st.markdown(
    """
    <div style="text-align:center; padding:5px;">
        <p style="color:#A0A0A0;">
            Intelligent Multilingual Speech Recognition
            and Analysis Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR SETTINGS
# ==========================================

with st.sidebar:

    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    # WHISPER MODEL

    st.markdown("### 🎙️ Whisper Model")

    model_size = st.selectbox(
        "Select transcription model",
        ["tiny", "base", "small", "medium"],
        index=0
    )

    st.caption(
        "Tiny model is recommended for computers "
        "with limited RAM."
    )

    st.markdown("---")

    # LANGUAGE SETTINGS

    st.markdown("### 🌐 Multilingual Settings")

    detection_mode = st.radio(
        "Language Detection Mode",
        [
            "Automatic Detection",
            "Manual Selection",
            "Both Automatic and Manual"
        ],
        index=0
    )

    selected_languages = []

    if detection_mode in [
        "Manual Selection",
        "Both Automatic and Manual"
    ]:

        selected_languages = st.multiselect(
            "Select languages in your audio",
            options=LANGUAGE_NAMES,
            default=[
                "Tamil",
                "English",
                "Hindi",
                "Malayalam",
                "Telugu",
                "Kannada"
            ],
            help=(
                "Choose all languages that may be spoken "
                "in your recording."
            )
        )

    if detection_mode == "Automatic Detection":

        st.info(
            "Whisper will automatically detect the "
            "dominant spoken language."
        )

    elif detection_mode == "Manual Selection":

        st.info(
            "Selected languages will be used as "
            "transcription hints."
        )

    else:

        st.info(
            "Automatic detection will be used together "
            "with your selected language hints."
        )

    st.markdown("---")

    # TRANSLATION SETTINGS

    st.markdown("### 🌍 Translation Settings")

    target_language = st.selectbox(
        "Translate transcript to",
        TRANSLATION_OPTIONS,
        index=0,
        help="Choose your required translation language."
    )

    st.caption(
        f"{len(TRANSLATION_LANGUAGE_MAP)} translation "
        "languages available, plus Tanglish."
    )

    if TRANSLATION_LIST_IS_FALLBACK:
        st.caption(
            "Showing the built-in translation language list."
        )

    st.markdown("---")

    # SPEAKER ANALYSIS

    st.markdown("### 👥 Speaker Analysis")

    enable_diarization = st.checkbox(
        "Enable Speaker Diarization",
        value=False,
        disabled=not SPEAKER_AVAILABLE
    )

    hf_token = ""

    if enable_diarization:
        hf_token = st.text_input(
            "Hugging Face Token",
            type="password"
        )

    if not SPEAKER_AVAILABLE:
        st.caption(
            "Speaker diarization modules are not available."
        )

    st.markdown("---")

    st.caption(
        "The first transcription may download "
        "the selected Whisper model."
    )

    st.caption(
        "SpeechFlow AI | Multilingual Audio Intelligence"
    )

# ==========================================
# AUDIO UPLOAD SECTION
# ==========================================

st.markdown("## 🎧 Upload Audio")

st.write(
    "Upload an audio recording containing one or "
    "multiple languages."
)

st.info(
    "Supported examples: Tamil + English (Tanglish), "
    "Hindi + English (Hinglish), Malayalam + English, "
    "Telugu + English and Kannada + English."
)

uploaded = st.file_uploader(
    "Choose your audio file",
    type=[
        "wav",
        "mp3",
        "m4a",
        "flac",
        "ogg",
        "mp4",
        "webm",
        "mpeg",
        "mpg"
    ],
    help="Upload your audio recording."
)

# ==========================================
# PROCESS UPLOADED AUDIO
# ==========================================

if uploaded is not None:

    suffix = Path(uploaded.name).suffix.lower()

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    saved_path = UPLOAD_DIR / f"current_upload{suffix}"

    saved_path.write_bytes(uploaded.getbuffer())

    # VALIDATE AUDIO

    valid, message = validate_audio(saved_path)

    if not valid:

        st.error(message)

    else:

        st.success("Audio uploaded successfully!")

        st.audio(uploaded)

        # AUDIO INFORMATION

        info = get_audio_info(saved_path)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "File Name",
            uploaded.name
        )

        col2.metric(
            "Duration",
            f"{info['duration_seconds']:.2f} sec"
            if info["duration_seconds"]
            else "Not available"
        )

        col3.metric(
            "Sample Rate",
            f"{info['sample_rate']} Hz"
            if info["sample_rate"]
            else "Not available"
        )

        st.divider()

        # ANALYZE AUDIO BUTTON

        if st.button(
            "🚀 Analyze Audio",
            type="primary",
            use_container_width=True
        ):

            # VALIDATE MANUAL SELECTION

            if (
                detection_mode == "Manual Selection"
                and not selected_languages
            ):

                st.error(
                    "Please select at least one language."
                )

                st.stop()

            # WHISPER LANGUAGE

            whisper_hint = None

            if (
                detection_mode == "Manual Selection"
                and len(selected_languages) == 1
            ):

                whisper_hint = LANGUAGE_CODES[
                    selected_languages[0]
                ]

            # TRANSCRIPTION

            with st.spinner(
                "Loading Whisper model and transcribing audio..."
            ):

                try:

                    result = transcribe_audio(
                        saved_path,
                        model_size=model_size,
                        language=whisper_hint,
                        selected_languages=selected_languages
                    )

                    transcript = result.get("text", "")

                    segments = result.get("segments", [])

                    whisper_language = result.get(
                        "language",
                        None
                    )

                    language_probability = result.get(
                        "language_probability",
                        None
                    )

                except Exception as exc:

                    st.error(
                        f"Transcription failed: {exc}"
                    )

                    st.stop()

            if not transcript.strip():

                st.warning(
                    "No speech detected. "
                    "Please upload another audio file."
                )

                st.stop()

            # LANGUAGE DETECTION

            try:

                detected_language = detect_language(
                    transcript,
                    whisper_language
                )

            except Exception:

                detected_language = (
                    whisper_language or "Unknown"
                )

            # SPEAKER IDENTIFICATION

            speaker_rows = []

            if enable_diarization:

                with st.spinner("Identifying speakers..."):

                    try:

                        raw_speakers = diarize_audio(
                            saved_path,
                            hf_token
                        )

                        speaker_rows = assign_speaker_labels(
                            raw_speakers
                        )

                    except Exception as exc:

                        st.warning(
                            f"Speaker analysis unavailable: {exc}"
                        )

            # CONVERSATION ANALYTICS

            try:

                insights = analyze_conversation(
                    transcript,
                    segments
                )

            except Exception as exc:

                st.warning(
                    f"Conversation analytics unavailable: {exc}"
                )

                insights = {}

            # EMOTION ANALYSIS

            try:

                emotion = analyze_emotion(transcript)

            except Exception as exc:

                st.warning(
                    f"Emotion analysis unavailable: {exc}"
                )

                emotion = {}

            # TEXT SUMMARIZATION

            try:

                summary = summarize_text(
                    transcript,
                    max_sentences=4
                )

            except Exception as exc:

                st.warning(
                    f"Summary unavailable: {exc}"
                )

                summary = ""

            # ==========================================
            # COMPLETE TEXT TRANSLATION
            # NO CHUNK SPLITTING
            # ==========================================

            translated = ""

            if target_language != "None":

                with st.spinner(
                    "Translating complete transcript..."
                ):

                    try:

                        translated = translate_text(
                            transcript,
                            target_language
                        )

                    except Exception as exc:

                        st.warning(
                            f"Translation unavailable: {exc}"
                        )

            # STORE ANALYSIS RESULTS

            analysis = {
                "filename": uploaded.name,
                "transcript": transcript,
                "segments": segments,
                "language": detected_language,
                "language_probability": language_probability,
                "selected_languages": selected_languages,
                "detection_mode": detection_mode,
                "speakers": speaker_rows,
                "conversation": insights,
                "emotion": emotion,
                "summary": summary,
                "translation": translated,
                "target_language": target_language
            }

            st.session_state["speechflow_analysis"] = analysis

            # SAVE ANALYSIS TO DATABASE

            try:

                save_session(
                    uploaded.name,
                    transcript,
                    detected_language,
                    info.get("duration_seconds", 0.0)
                )

                st.success(
                    "Analysis completed and session saved!"
                )

            except Exception as exc:

                st.warning(
                    "Analysis completed, but session "
                    f"could not be saved: {exc}"
                )

# ==========================================
# DISPLAY ANALYSIS RESULTS
# ==========================================

if "speechflow_analysis" in st.session_state:

    data = st.session_state["speechflow_analysis"]

    st.divider()

    st.markdown("## 📊 Analysis Results")

    st.caption(
        f"File: {data['filename']} | "
        f"Detected Language: {data['language']}"
    )

    st.write(
        f"**Detection Mode:** {data['detection_mode']}"
    )

    if data["selected_languages"]:

        st.write(
            "**Selected Languages:** "
            + ", ".join(data["selected_languages"])
        )

    if data["language_probability"] is not None:

        st.write(
            f"**Detection Confidence:** "
            f"{data['language_probability']:.2%}"
        )

    # RESULT TABS

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📝 Transcript",
            "📌 Summary",
            "👥 Speakers",
            "📊 Analytics",
            "📄 Export"
        ]
    )

    # TAB 1 - TRANSCRIPT

    with tab1:

        st.markdown("### 📝 Speech Transcript")

        show_transcript(data["transcript"])

        st.download_button(
            "⬇️ Download Transcript",
            data["transcript"],
            file_name="speechflow_transcript.txt",
            mime="text/plain",
            use_container_width=True
        )

        if data["translation"]:

            st.markdown("### 🌐 Translated Transcript")

            st.text_area(
                "Translation",
                data["translation"],
                height=200
            )

            st.download_button(
                "⬇️ Download Translation",
                data["translation"],
                file_name="speechflow_translation.txt",
                mime="text/plain"
            )

    # TAB 2 - SUMMARY

    with tab2:

        st.markdown("### 📌 AI-Assisted Summary")

        if data["summary"]:

            st.info(data["summary"])

        else:

            st.warning("No summary available.")

        st.markdown("### 📄 Full Transcript")

        st.write(data["transcript"])

    # TAB 3 - SPEAKER ANALYSIS

    with tab3:

        st.markdown("### 👥 Speaker Diarization")

        if data["speakers"]:

            st.dataframe(
                data["speakers"],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Speaker diarization has not been performed. "
                "Enable it in Settings to identify speaker turns."
            )

    # TAB 4 - ANALYTICS

    with tab4:

        st.markdown("### 📊 Conversation Analytics")

        show_analytics(data["conversation"])

        st.divider()

        st.markdown("### 🧠 Text Tone Estimation")

        st.json(data["emotion"])

        st.caption(
            "This is a basic keyword-based text estimate, "
            "not vocal emotion recognition or a clinical assessment."
        )

        st.divider()

        st.markdown("### 🎯 Speech Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Words",
            data["conversation"].get("word_count", 0)
        )

        col2.metric(
            "Total Sentences",
            data["conversation"].get("sentence_count", 0)
        )

        col3.metric(
            "Words Per Minute",
            data["conversation"].get("words_per_minute") or "N/A"
        )

    # TAB 5 - EXPORT REPORT

    with tab5:

        st.markdown("### 📄 Download Analysis Report")

        try:

            report_text = create_report(data)

            st.download_button(
                "⬇️ Download Complete Report",
                report_text,
                file_name="speechflow_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as exc:

            st.error(
                f"Report generation failed: {exc}"
            )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px;
        color:#A0A0A0;
    ">
        <h4 style="color:#A31C1B;">
            🎙️ SpeechFlow AI
        </h4>
        <p>
            Listen • Understand • Analyze
        </p>
        <p style="font-size:12px;">
            Multilingual Speech Recognition Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
