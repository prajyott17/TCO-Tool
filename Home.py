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

/* ===== FULL PAGE ===== */

.stApp{

    background:
        linear-gradient(
            180deg,
            #0b1120 0%,
            #111827 100%
        );
}

/* remove white block */

[data-testid="stAppViewContainer"]{

    background:transparent;
}

.main .block-container{

    max-width:1180px;

    padding-top:20px;

    padding-bottom:40px;
}

/* ===== HERO ===== */

.hero{

    margin-top:10px;

    margin-bottom:38px;
}

.hero-badge{

    display:inline-block;

    padding:7px 14px;

    border-radius:999px;

    background:
        rgba(59,130,246,0.12);

    border:
        1px solid rgba(59,130,246,0.20);

    color:#60a5fa;

    font-size:12px;

    font-weight:600;

    margin-bottom:18px;
}

.hero-title{

    font-size:42px;

    font-weight:780;

    letter-spacing:-1px;

    color:white;

    margin-bottom:14px;
}

.hero-title span{

    color:#3b82f6;
}

.hero-sub{

    max-width:720px;

    font-size:15px;

    line-height:1.9;

    color:#94a3b8;
}

/* ===== SECTION ===== */

.section-title{

    font-size:22px;

    font-weight:700;

    color:white;

    margin-bottom:20px;
}

/* ===== GRID ===== */

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:22px;
}

/* ===== CARD ===== */

.card{

    position:relative;

    padding:24px;

    border-radius:18px;

    background:
        rgba(17,24,39,0.75);

    backdrop-filter:blur(12px);

    border:
        1px solid rgba(255,255,255,0.06);

    transition:0.25s ease;

    overflow:hidden;
}

/* glow */

.card::before{

    content:"";

    position:absolute;

    width:140px;
    height:140px;

    background:
        rgba(37,99,235,0.15);

    border-radius:50%;

    top:-60px;
    right:-60px;

    filter:blur(25px);
}

.card:hover{

    transform:
        translateY(-4px);

    border:
        1px solid rgba(59,130,246,0.25);

    box-shadow:
        0 14px 34px rgba(37,99,235,0.12);
}

/* ===== LABEL ===== */

.label{

    position:relative;
    z-index:2;

    font-size:11px;

    letter-spacing:1.5px;

    text-transform:uppercase;

    color:#60a5fa;

    margin-bottom:14px;
}

/* ===== TITLE ===== */

.title{

    position:relative;
    z-index:2;

    font-size:26px;

    font-weight:720;

    line-height:1.2;

    color:white;

    margin-bottom:14px;
}

/* ===== DESC ===== */

.desc{

    position:relative;
    z-index:2;

    font-size:14px;

    line-height:1.8;

    color:#9ca3af;

    margin-bottom:24px;
}

/* ===== BUTTON ===== */

.btn{

    position:relative;
    z-index:2;

    display:inline-block;

    padding:10px 18px;

    border-radius:12px;

    background:#2563eb;

    color:white !important;

    text-decoration:none;

    font-size:13px;

    font-weight:650;

    transition:0.2s ease;
}

.btn:hover{

    background:#3b82f6;
}

/* ===== FOOTER ===== */

.footer{

    margin-top:50px;

    padding-top:16px;

    border-top:
        1px solid rgba(255,255,255,0.06);

    color:#6b7280;

    font-size:12px;
}

</style>

<div class="hero">

<div class="hero-badge">
Enterprise Analytics Platform
</div>

<div class="hero-title">
TCO <span>Intelligence</span> Platform
</div>

<div class="hero-sub">
Operational analytics platform for lifecycle cost optimization,
maintenance intelligence, rental evaluation,
and compressor ownership analysis.
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