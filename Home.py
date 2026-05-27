import streamlit as st

st.set_page_config(page_title="My Tools", layout="wide")
from utils import load_css
load_css()
from nav import top_nav
top_nav("home")
st.markdown("""
<style>

/* Main container */
[data-testid="stAppViewContainer"] .block-container {
    max-width: 1100px;
    padding: 20px;
    margin-top: 60px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    width: 250px !important;
    padding-top: 20px;
}

/* Fix gap */
[data-testid="stAppViewContainer"] .main {
    margin-left: 0px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h3 style='margin-bottom: 10px;'>🚀 Tools Dashboard</h3>
""", unsafe_allow_html=True)

st.markdown("""
##### Available Tools

- 🛠️ TCO (Genuine vs Non-Genuine)
- 🏗️ Rental
            
""")