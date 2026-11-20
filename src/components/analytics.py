@'
import streamlit as st


def show_analytics(analytics):

    st.markdown("### Conversation Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Words",
        analytics.get("word_count", 0)
    )

    col2.metric(
        "Sentences",
        analytics.get("sentence_count", 0)
    )

    speed = analytics.get("words_per_minute")

    col3.metric(
        "Words Per Minute",
        speed if speed is not None else "N/A"
    )

    st.markdown("### Frequently Used Words")

    frequent = analytics.get("frequent_words", [])

    if frequent:
        chart_data = {
            item["word"]: item["count"]
            for item in frequent
        }
        st.bar_chart(chart_data)
    else:
        st.info("No frequent words to display.")
'@ | Set-Content -Path ".\components\analytics.py" -Encoding utf8