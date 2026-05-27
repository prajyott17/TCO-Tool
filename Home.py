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

/* ================= PAGE ================= */

.stApp{

    background:
        linear-gradient(
            180deg,
            #f8fbff 0%,
            #eef4ff 100%
        );
}

/* Main width */

.main-wrap{

    max-width:1180px;

    margin:auto;

    padding-top:0px;
}

/* ================= HERO ================= */

.hero{

    margin-top:10px;

    margin-bottom:42px;
}

.hero-badge{

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:8px 16px;

    border-radius:999px;

    background:
        rgba(37,99,235,0.08);

    color:#2563eb;

    font-size:13px;

    font-weight:650;

    margin-bottom:22px;
}

.hero-title{

    font-size:64px;

    font-weight:850;

    letter-spacing:-2.5px;

    line-height:1.02;

    color:#0f172a;

    margin-bottom:20px;
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

    font-size:18px;

    line-height:1.9;

    color:#64748b;
}

/* ================= SECTION ================= */

.section-title{

    font-size:28px;

    font-weight:760;

    color:#0f172a;

    margin-bottom:24px;
}

/* ================= GRID ================= */

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:24px;
}

/* ================= CARD ================= */

.card{

    position:relative;

    overflow:hidden;

    padding:28px;

    min-height:250px;

    border-radius:22px;

    background:
        rgba(255,255,255,0.75);

    backdrop-filter:blur(16px);

    border:
        1px solid rgba(255,255,255,0.45);

    box-shadow:
        0 12px 30px rgba(15,23,42,0.06);

    transition:all 0.25s ease;
}

/* Top Accent */

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
            #06b6d4
        );
}

/* Glow */

.card::after{

    content:"";

    position:absolute;

    width:180px;
    height:180px;

    border-radius:50%;

    background:
        rgba(37,99,235,0.10);

    top:-70px;
    right:-70px;

    filter:blur(30px);
}

.card:hover{

    transform:
        translateY(-6px);

    box-shadow:
        0 24px 50px rgba(37,99,235,0.12);
}

/* ================= SMALL LABEL ================= */

.label{

    position:relative;
    z-index:2;

    font-size:12px;

    font-weight:700;

    letter-spacing:2px;

    text-transform:uppercase;

    color:#3b82f6;

    margin-bottom:20px;
}

/* ================= TITLE ================= */

.title{

    position:relative;
    z-index:2;

    font-size:34px;

    font-weight:780;

    line-height:1.15;

    color:#0f172a;

    margin-bottom:16px;
}

/* ================= DESC ================= */

.desc{

    position:relative;
    z-index:2;

    font-size:15px;

    line-height:1.9;

    color:#64748b;

    max-width:470px;

    margin-bottom:28px;
}

/* ================= BUTTON ================= */

.btn{

    position:relative;
    z-index:2;

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:12px 22px;

    border-radius:14px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );

    color:white !important;

    text-decoration:none;

    font-size:14px;

    font-weight:700;

    box-shadow:
        0 10px 24px rgba(37,99,235,0.18);

    transition:all 0.2s ease;
}

.btn:hover{

    transform:
        translateY(-2px);

    box-shadow:
        0 16px 34px rgba(37,99,235,0.26);
}

/* ================= FOOTER ================= */

.footer{

    margin-top:60px;

    padding-top:18px;

    border-top:
        1px solid rgba(148,163,184,0.18);

    color:#94a3b8;

    font-size:13px;
}

</style>

<div class="main-wrap">

<!-- HERO -->

<div class="hero">

<div class="hero-badge">
⚡ Enterprise Analytics Platform
</div>

<div class="hero-title">
TCO <span>Intelligence</span> Platform
</div>

<div class="hero-sub">

Advanced lifecycle cost analytics platform for compressor operations,
maintenance optimization, downtime intelligence,
and rental profitability analysis.

</div>

</div>

<!-- SECTION -->

<div class="section-title">
Available Tools
</div>

<!-- GRID -->

<div class="grid">

<!-- CARD 1 -->

<div class="card">

<div class="label">
Lifecycle Analytics
</div>

<div class="title">
TCO Genuine vs Non-Genuine
</div>

<div class="desc">

Analyze lifecycle ownership cost, downtime exposure,
maintenance quality, overhaul impact,
and operational efficiency.

</div>

<a class="btn" href="?page=tco_genuine" target="_self">
Open Tool →
</a>

</div>

<!-- CARD 2 -->

<div class="card">

<div class="label">
Rental Intelligence
</div>

<div class="title">
Rental Calculator
</div>

<div class="desc">

Evaluate rental profitability, utilization efficiency,
operating cost exposure,
and ownership recovery analysis.

</div>

<a class="btn" href="?page=rental" target="_self">
Open Tool →
</a>

</div>

</div>

<!-- FOOTER -->

<div class="footer">
Chicago Pneumatic • Internal Business Platform
</div>

</div>

""", unsafe_allow_html=True)