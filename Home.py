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

section[data-testid="stSidebar"]{
    display:none !important;
}

[data-testid="stSidebarCollapsedControl"]{
    display:none !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""

<style>

/* ===== APP BACKGROUND ===== */

.stApp{

    background:
        linear-gradient(
            180deg,
            #f5f7fb 0%,
            #eef3ff 100%
        );
}

/* ===== MAIN CONTAINER ===== */

.main .block-container{

    max-width:1180px;

    padding-top:15px;

    padding-bottom:40px;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"]{

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f8fbff 100%
        );

    border-right:
        1px solid #e2e8f0;
}

/* ===== HEADER ===== */

header{

    background:
        rgba(255,255,255,0.75) !important;

    backdrop-filter:blur(12px);
}

/* ===== HERO ===== */

.hero{

    margin-top:10px;

    margin-bottom:36px;
}

.badge{

    display:inline-block;

    padding:7px 14px;

    border-radius:999px;

    background:
        rgba(37,99,235,0.10);

    color:#2563eb;

    font-size:12px;

    font-weight:650;

    margin-bottom:18px;
}

.hero-title{

    font-size:46px;

    font-weight:800;

    letter-spacing:-1px;

    line-height:1.05;

    color:#0f172a;

    margin-bottom:14px;
}

.hero-title span{

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #06b6d4
        );

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;
}

.hero-sub{

    max-width:760px;

    font-size:15px;

    line-height:1.9;

    color:#64748b;
}

/* ===== SECTION ===== */

.section-title{

    font-size:24px;

    font-weight:750;

    color:#0f172a;

    margin-bottom:20px;
}

/* ===== GRID ===== */

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:24px;
}

/* ===== CARDS ===== */

.card{

    position:relative;

    overflow:hidden;

    padding:26px;

    border-radius:22px;

    background:
        rgba(255,255,255,0.78);

    backdrop-filter:blur(14px);

    border:
        1px solid rgba(255,255,255,0.65);

    box-shadow:
        0 10px 30px rgba(15,23,42,0.06);

    transition:all 0.25s ease;
}

/* subtle top glow */

.card::before{

    content:"";

    position:absolute;

    left:0;
    top:0;

    width:100%;
    height:5px;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #38bdf8
        );
}

/* glow orb */

.card::after{

    content:"";

    position:absolute;

    width:140px;
    height:140px;

    border-radius:50%;

    background:
        rgba(59,130,246,0.10);

    top:-50px;
    right:-50px;

    filter:blur(24px);
}

.card:hover{

    transform:
        translateY(-4px);

    box-shadow:
        0 18px 40px rgba(37,99,235,0.12);
}

/* ===== LABEL ===== */

.label{

    position:relative;
    z-index:2;

    font-size:11px;

    font-weight:700;

    letter-spacing:1.5px;

    text-transform:uppercase;

    color:#3b82f6;

    margin-bottom:14px;
}

/* ===== TITLE ===== */

.title{

    position:relative;
    z-index:2;

    font-size:28px;

    font-weight:760;

    line-height:1.2;

    color:#0f172a;

    margin-bottom:14px;
}

/* ===== DESC ===== */

.desc{

    position:relative;
    z-index:2;

    font-size:14px;

    line-height:1.8;

    color:#64748b;

    margin-bottom:24px;
}

/* ===== BUTTON ===== */

.btn{

    position:relative;
    z-index:2;

    display:inline-block;

    padding:10px 18px;

    border-radius:12px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );

    color:white !important;

    text-decoration:none;

    font-size:13px;

    font-weight:650;

    box-shadow:
        0 8px 20px rgba(37,99,235,0.16);

    transition:all 0.2s ease;
}

.btn:hover{

    transform:
        translateY(-2px);

    box-shadow:
        0 14px 28px rgba(37,99,235,0.20);
}

/* ===== FOOTER ===== */

.footer{

    margin-top:55px;

    padding-top:18px;

    border-top:
        1px solid rgba(148,163,184,0.18);

    color:#94a3b8;

    font-size:12px;
}

</style>

<div class="hero">

<div class="badge">
Enterprise Analytics Platform
</div>

</div>

<div class="section-title">
Available Tools
</div>

<div class="grid">

<div class="card">

<div class="label">
Lifecycle Analytics
</div>

<div class="title">
TCO Genuine vs Non-Genuine
</div>

<div class="desc">
Analyze lifecycle ownership cost,
maintenance quality, downtime exposure,
and operational efficiency.
</div>

<a class="btn" href="?page=tco_genuine" target="_self">
Open Tool
</a>

</div>

<div class="card">

<div class="label">
Rental Intelligence
</div>

<div class="title">
Rental Calculator
</div>

<div class="desc">
Evaluate rental profitability,
utilization efficiency,
and ownership recovery analysis.
</div>

<a class="btn" href="?page=rental" target="_self">
Open Tool
</a>

</div>

</div>

<div class="footer">
Chicago Pneumatic • Internal Business Platform
</div>

""", unsafe_allow_html=True)