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

/* ===== PAGE ===== */

.main-container{
    max-width:1250px;
    margin:auto;
    padding-top:10px;
}

/* ===== HERO ===== */

.hero{

    padding:55px;

    border-radius:30px;

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 45%,
            #2563eb 100%
        );

    position:relative;

    overflow:hidden;

    margin-bottom:45px;

    box-shadow:
        0 20px 50px rgba(37,99,235,0.22);
}

/* Glow */

.hero::before{

    content:"";

    position:absolute;

    width:420px;
    height:420px;

    background:rgba(255,255,255,0.08);

    border-radius:50%;

    top:-140px;
    right:-120px;
}

/* ===== TEXT ===== */

.hero-title{

    font-size:52px;

    font-weight:800;

    color:white;

    line-height:1.1;

    margin-bottom:16px;

    position:relative;
    z-index:2;
}

.hero-subtitle{

    font-size:18px;

    color:#dbeafe;

    line-height:1.8;

    max-width:760px;

    position:relative;
    z-index:2;
}

/* ===== SECTION ===== */

.section-title{

    font-size:28px;

    font-weight:750;

    color:#0f172a;

    margin-bottom:26px;
}

/* ===== TOOL GRID ===== */

.tool-grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:28px;
}

/* ===== CARD ===== */

.tool-card{

    position:relative;

    overflow:hidden;

    padding:34px;

    border-radius:28px;

    background:white;

    border:1px solid #e2e8f0;

    transition:all 0.28s ease;

    box-shadow:
        0 10px 30px rgba(15,23,42,0.06);
}

/* Top Gradient Line */

.tool-card::before{

    content:"";

    position:absolute;

    left:0;
    top:0;

    width:100%;
    height:6px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4,
        #8b5cf6
    );
}

.tool-card:hover{

    transform:
        translateY(-8px)
        scale(1.01);

    box-shadow:
        0 24px 60px rgba(37,99,235,0.12);
}

/* ===== ICON ===== */

.tool-icon{

    width:72px;
    height:72px;

    border-radius:20px;

    display:flex;
    align-items:center;
    justify-content:center;

    font-size:34px;

    margin-bottom:24px;

    background:linear-gradient(
        135deg,
        #dbeafe,
        #eff6ff
    );
}

/* ===== TITLES ===== */

.tool-name{

    font-size:28px;

    font-weight:750;

    color:#0f172a;

    margin-bottom:14px;
}

/* ===== DESC ===== */

.tool-desc{

    font-size:15px;

    color:#64748b;

    line-height:1.9;

    margin-bottom:26px;
}

/* ===== BUTTON ===== */

.tool-btn{

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:12px 22px;

    border-radius:14px;

    background:linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color:white !important;

    text-decoration:none;

    font-size:14px;

    font-weight:650;

    transition:all 0.2s ease;
}

.tool-btn:hover{

    transform:translateY(-2px);

    box-shadow:
        0 10px 24px rgba(37,99,235,0.25);
}

/* ===== FOOTER ===== */

.footer{

    margin-top:70px;

    padding-top:20px;

    border-top:1px solid #e2e8f0;

    color:#94a3b8;

    font-size:13px;
}

</style>

<div class="main-container">

<div class="hero">

<div class="hero-title">
🚀 TCO Intelligence Platform
</div>

<div class="hero-subtitle">

Advanced lifecycle cost analytics platform for
compressor operations, maintenance optimization,
downtime intelligence, and rental profitability analysis.

</div>

</div>

<div class="section-title">
Available Tools
</div>

<div class="tool-grid">

<!-- CARD 1 -->

<div class="tool-card">

<div class="tool-icon">
🛠️
</div>

<div class="tool-name">
TCO Genuine vs Non-Genuine
</div>

<div class="tool-desc">

Compare lifecycle ownership cost across fuel,
maintenance, overhaul exposure, downtime impact,
breakdowns, and replacement frequency.

</div>

<a class="tool-btn" href="?page=tco_genuine" target="_self">
Open Tool →
</a>

</div>

<!-- CARD 2 -->

<div class="tool-card">

<div class="tool-icon">
🏗️
</div>

<div class="tool-name">
Rental Calculator
</div>

<div class="tool-desc">

Evaluate rental profitability, utilization efficiency,
operating cost exposure, and ownership recovery
under different machine operating conditions.

</div>

<a class="tool-btn" href="?page=rental" target="_self">
Open Tool →
</a>

</div>

</div>

<div class="footer">
TCO Analytics Platform • Internal Business Tool
</div>

</div>

""", unsafe_allow_html=True)