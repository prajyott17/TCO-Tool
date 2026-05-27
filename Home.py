import streamlit as st
from utils import load_css
from nav import top_nav

st.set_page_config(
    page_title="TCO Platform",
    layout="wide"
)

load_css()
top_nav("home")

st.markdown("""
<style>

.main-container{
    max-width:1200px;
    margin:auto;
    padding-top:20px;
}

/* HERO */

.hero{
    padding:40px 10px 20px 10px;
}

.hero-title{
    font-size:42px;
    font-weight:750;
    color:#0f172a;
    margin-bottom:12px;
}

.hero-subtitle{
    font-size:17px;
    color:#475569;
    max-width:760px;
    line-height:1.7;
}

/* SECTION */

.section-title{
    margin-top:35px;
    margin-bottom:20px;

    font-size:24px;
    font-weight:700;

    color:#0f172a;
}

/* TOOL GRID */

.tool-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:24px;
}

/* CARD */

.tool-card{
    background:white;

    border:1px solid #e2e8f0;

    border-radius:22px;

    padding:28px;

    transition:all 0.2s ease;

    box-shadow:
        0 4px 16px rgba(15,23,42,0.04);
}

.tool-card:hover{

    transform:translateY(-3px);

    box-shadow:
        0 14px 30px rgba(15,23,42,0.08);
}

/* ICON */

.tool-icon{
    font-size:38px;
    margin-bottom:16px;
}

/* TITLE */

.tool-name{
    font-size:22px;
    font-weight:700;
    color:#0f172a;
    margin-bottom:10px;
}

/* DESC */

.tool-desc{
    font-size:14px;
    color:#64748b;
    line-height:1.7;
    margin-bottom:22px;
}

/* BUTTON */

.tool-btn{

    display:inline-block;

    padding:10px 18px;

    border-radius:12px;

    background:#2563eb;

    color:white !important;

    text-decoration:none;

    font-size:14px;

    font-weight:600;
}

.tool-btn:hover{
    background:#1d4ed8;
}

/* FOOTER */

.footer{
    margin-top:60px;
    padding-top:18px;

    border-top:1px solid #e2e8f0;

    font-size:13px;

    color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# HERO

st.markdown("""

<div class="main-container">

<div class="section-title">
Available Tools
</div>

<div class="tool-grid">

<div class="tool-card">

<div class="tool-icon">
🛠️
</div>

<div class="tool-name">
TCO Genuine vs Non-Genuine
</div>

<div class="tool-desc">
Analyze lifecycle ownership cost across fuel consumption,
maintenance strategy, overhaul exposure, downtime impact,
and replacement frequency.
</div>

<a class="tool-btn" href="?page=tco_genuine" target="_self">
Open Tool
</a>

</div>

<div class="tool-card">

<div class="tool-icon">
🏗️
</div>

<div class="tool-name">
Rental Calculator
</div>

<div class="tool-desc">
Evaluate rental profitability, operating cost,
utilization efficiency, and ownership recovery across
different machine operating conditions.
</div>

<a class="tool-btn" href="?page=rental" target="_self">
Open Tool
</a>

</div>

</div>

<div class="footer">
TCO Analytics Platform • Internal Business Tool
</div>

</div>

""", unsafe_allow_html=True)