import streamlit as st


def show_transcript(text):

    st.markdown("### Recognized Speech")

    if text and text.strip():

        st.text_area(
            "Transcribed Text",
            value=text,
            height=300,
            key="speechflow_transcript"
        )

        word_count = len(text.split())

        st.caption(f"Total words: {word_count}")

    else:

        st.info("No speech was detected in this recording.")
