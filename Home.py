import streamlit as st
from utils import load_css
from nav import top_nav

st.set_page_config(
    page_title="TCO Platform",
    layout="wide"
)

load_css()
top_nav("home")

# ================= HERO =================

st.markdown("""
<style>

.hero-section{
    padding:40px;
    border-radius:24px;

    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e3a8a 45%,
        #2563eb 100%
    );

    color:white;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.25);

    margin-bottom:30px;
}

.hero-title{
    font-size:42px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:12px;
}

.hero-subtitle{
    font-size:18px;
    color:#dbeafe;
    max-width:750px;
}

.metric-strip{
    display:flex;
    gap:16px;
    margin-top:28px;
}

.metric-card{
    flex:1;
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:18px;
    padding:18px;
    backdrop-filter: blur(10px);
}

.metric-title{
    font-size:13px;
    color:#cbd5e1;
    margin-bottom:6px;
}

.metric-value{
    font-size:24px;
    font-weight:700;
}

.tool-title{
    font-size:28px;
    font-weight:700;
    margin-bottom:20px;
    color:#0f172a;
}

.tool-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:22px;
}

.tool-card{
    padding:28px;
    border-radius:22px;
    background:white;
    border:1px solid #e2e8f0;

    box-shadow:
        0 8px 24px rgba(15,23,42,0.05);

    transition: all 0.2s ease;
}

.tool-card:hover{
    transform: translateY(-4px);

    box-shadow:
        0 18px 40px rgba(15,23,42,0.10);
}

.tool-icon{
    font-size:42px;
    margin-bottom:14px;
}

.tool-name{
    font-size:22px;
    font-weight:700;
    color:#0f172a;
    margin-bottom:10px;
}

.tool-desc{
    font-size:14px;
    color:#475569;
    line-height:1.6;
    margin-bottom:20px;
}

.launch-btn{
    display:inline-block;
    padding:10px 18px;
    border-radius:12px;

    background:linear-gradient(
        135deg,
        #2563eb 0%,
        #1d4ed8 100%
    );

    color:white !important;
    text-decoration:none;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ================= HERO =================

st.markdown("""
<div class="hero-section">

<div class="hero-title">
🚀 Total Cost of Ownership Platform
</div>

<div class="hero-subtitle">
Advanced operational intelligence platform for compressor lifecycle analysis,
maintenance optimization, rental evaluation, and cost benchmarking.
</div>

<div class="metric-strip">

<div class="metric-card">
<div class="metric-title">Fuel Optimization</div>
<div class="metric-value">14%</div>
</div>

<div class="metric-card">
<div class="metric-title">Downtime Reduction</div>
<div class="metric-value">35%</div>
</div>

<div class="metric-card">
<div class="metric-title">Maintenance Savings</div>
<div class="metric-value">₹12L+</div>
</div>

<div class="metric-card">
<div class="metric-title">Operational Visibility</div>
<div class="metric-value">100%</div>
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ================= TOOLS =================

st.markdown(
    '<div class="tool-title">Available Tools</div>',
    unsafe_allow_html=True
)

st.markdown("""

<div class="tool-grid">

<div class="tool-card">

<div class="tool-icon">🛠️</div>

<div class="tool-name">
TCO Genuine vs Non-Genuine
</div>

<div class="tool-desc">
Compare lifecycle cost impact of genuine versus non-genuine maintenance
strategies including fuel, overhaul, downtime, breakdown, and replacement analysis.
</div>

<a class="launch-btn" href="?page=tco_genuine" target="_self">
Launch Tool
</a>

</div>

<div class="tool-card">

<div class="tool-icon">🏗️</div>

<div class="tool-name">
Rental Calculator
</div>

<div class="tool-desc">
Analyze rental economics, utilization efficiency, operating cost exposure,
and profitability across varying project durations and machine loads.
</div>

<a class="launch-btn" href="?page=rental" target="_self">
Launch Tool
</a>

</div>

</div>

""", unsafe_allow_html=True)