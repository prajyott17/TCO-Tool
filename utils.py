import streamlit as st
import requests
import certifi

@st.cache_data(ttl=3600)
def get_rate(base="INR"):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        res = requests.get(url, timeout=5, verify=certifi.where())
        return res.json()["rates"]
    except Exception:
        return {"USD": 93, "EUR": 109}
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)