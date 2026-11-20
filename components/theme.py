
import streamlit as st


def apply_custom_theme():
    st.markdown(
        """
        <style>
        /* Main application background */
        .stApp {
            background-color: #121212;
            color: #FFFFFF;
        }

        /* Main headings */
        h1, h2, h3 {
            color: #228B22 !important;
            font-weight: 700;
        }

        /* Paragraphs and labels */
        p, label, span {
            color: #F5F5F5;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1B1B1B;
        }

        /* Buttons */
        .stButton > button {
            background-color: #DC143C;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #228B22;
            color: white;
        }

        /* Text input */
        .stTextInput input,
        .stTextArea textarea {
            background-color: #252525;
            color: white;
            border: 1px solid #228B22;
        }

        /* Cards */
        .custom-card {
            background-color: #202020;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #228B22;
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
