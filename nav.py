import streamlit as st
from utils import get_rate

st.set_page_config(layout="wide")
from utils import load_css
from PIL import Image

load_css()

def top_nav(current_page):
    header_col1, header_col2 = st.columns([1.2, 6])

    with header_col1:
        st.image("assets/chicago-pneumatic.jpg", width=110)

    rates = get_rate()
    usd = rates["USD"]
    eur = rates["EUR"]

    params = st.query_params
    page = params.get("page")

    if page == "home" and current_page != "home":
        st.switch_page("Home.py")

    elif page == "tco" and current_page != "tco":
        st.switch_page("pages/1_TCO_Tool.py")

    elif page == "tco_genuine" and current_page != "tco_genuine":
        st.switch_page("pages/2_TCO_Genuine_vs_Non_Genuine.py")

    elif page == "rental" and current_page != "rental":
        st.switch_page("pages/3_Rental_Calculator.py")

    

    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-bottom: 1px solid #ddd;
        margin-bottom: 10px;
    }

    .tabs {
        display: flex;
        gap: 6px;
    }

    .tab {
        padding: 6px 16px;
        font-size: 14px;
        background: #eaeaea;
        border: 1px solid #ddd;
        border-bottom: none;
        border-radius: 8px 8px 0 0;
        text-decoration: none;
        color: black;
    }

    .tab.active {
        background: white;
        font-weight: 600;
        border-bottom: 1px solid white;
        margin-bottom: -1px;
    }

    .tab:hover {
        background: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([7,2,1])

    # ===== Tabs =====
    with col1:
        st.markdown(f"""
        <div class="nav-container">
            <div class="tabs">
                <a href="?page=home" target="_self" class="tab {'active' if current_page=='home' else ''}">🏠 Home</a>
                <a href="?page=tco_genuine" target="_self" class="tab {'active' if current_page=='tco_genuine' else ''}">🛠️ TCO(Genuine vs Non-Genuine)</a>
                <a href="?page=rental" target="_self" class="tab {'active' if current_page=='rental' else ''}">⛽ Rental</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    currency = None

# ===== Show dropdown for TCO + TCO Genuine =====
    if current_page in ["tco", "tco_genuine", "rental"]:
        with col2:
            if "global_currency" not in st.session_state:
                st.session_state.global_currency = "INR (₹)"

            currency = st.selectbox(
                "Currency",
                ["INR (₹)", "USD ($)", "EURO (€)"],

                key="global_currency",

                label_visibility="collapsed"
            )
        with col3:
            st.markdown(
                f"""
                <div style='text-align:right; font-size:12px; color:gray;'>
                1 USD = ₹{usd:.2f}<br>
                1 EUR = ₹{eur:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        with col2:
            st.empty()
    return currency