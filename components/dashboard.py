import streamlit as st

def show_dashboard(title="SpeechFlow AI"):
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #06110C, #171717, #A31C1B);
            border: 1px solid #A31C1B;
            border-radius: 18px;
            padding: 35px;
            text-align: center;
        ">
            <h1 style="color:white;">🎙️ SpeechFlow AI</h1>
            <p style="color:white;">Intelligent Speech Analysis Platform</p>
            <p style="color:#E8A09E;">LISTEN • UNDERSTAND • ANALYZE</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_metric(label, value, icon="📊"):
    st.metric(label, value)
