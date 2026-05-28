import streamlit as st
import base64
@st.cache_data(ttl=3600)
def get_rate():
    return {
        "USD": 93,
        "EUR": 109
    }
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        