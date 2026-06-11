import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    .stApp {
        background: radial-gradient(
        circle at center,
        #020617,
        #000000
        );
        color:white;
    }

    h1 {
        color:#22d3ee;
        text-align:center;
    }

    </style>
    """,unsafe_allow_html=True)
