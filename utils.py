import streamlit as st
import base64

def image_to_base64(path):

    with open(path, "rb") as img:
        return base64.b64encode(
            img.read()
        ).decode()
@st.cache_data(ttl=3600)
def get_rate():
    return {
        "USD": 93,
        "EUR": 109
    }
def load_css():

    with open("assets/logo.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    machine = image_to_base64(
        "assets/tool_machine.png"
    )

    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace(
        "CP_BACKGROUND_IMAGE",
        f"data:image/png;base64,{encoded}"
    )

    css = css.replace(
        "TCO_MACHINE",
        f"data:image/jpeg;base64,{machine}"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
