import streamlit as st
import base64

@st.cache_data(ttl=3600)
def get_rate():
    return {
        "USD": 93,
        "EUR": 109
    }

def load_css():

    with open("assets/cp_bg.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace(
        "CP_BACKGROUND_IMAGE",
        f"data:image/png;base64,{encoded}"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )

