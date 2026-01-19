import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        .main { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )  # [file:1]
