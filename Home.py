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

.stApp{
    background:
        radial-gradient(circle at top left,
        #172554 0%,
        #0b1120 45%);

    color:white;
}

/* MAIN */

.main-wrap{
    max-width:1180px;
    margin:auto;
    padding-top:30px;
}

/* HERO */

.hero-title{

    font-size:56px;

    font-weight:800;

    letter-spacing:-2px;

    color:white;

    margin-bottom:12px;
}

.hero-sub{

    font-size:18px;

    color:#94a3b8;

    max-width:720px;

    line-height:1.8;

    margin-bottom:60px;
}

/* TOOL GRID */

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:24px;
}

/* CARD */

.card{

    position:relative;

    padding:32px;

    border-radius:28px;

    background:
        rgba(15,23,42,0.65);

    backdrop-filter:blur(18px);

    border:
        1px solid rgba(255,255,255,0.08);

    transition:0.25s ease;

    overflow:hidden;
}

.card:hover{

    transform:
        translateY(-6px);

    border:
        1px solid rgba(59,130,246,0.45);

    box-shadow:
        0 0 40px rgba(37,99,235,0.18);
}

/* GLOW */

.card::before{

    content:"";

    position:absolute;

    width:180px;
    height:180px;

    background:
        rgba(37,99,235,0.18);

    border-radius:50%;

    top:-80px;
    right:-80px;

    filter:blur(40px);
}

/* SMALL LABEL */

.label{

    font-size:12px;

    color:#60a5fa;

    text-transform:uppercase;

    letter-spacing:2px;

    margin-bottom:18px;

    position:relative;
    z-index:2;
}

/* TITLE */

.title{

    font-size:30px;

    font-weight:750;

    color:white;

    margin-bottom:16px;

    position:relative;
    z-index:2;
}

/* DESC */

.desc{

    color:#94a3b8;

    line-height:1.8;

    font-size:15px;

    margin-bottom:28px;

    position:relative;
    z-index:2;
}

/* BUTTON */

.btn{

    display:inline-flex;

    align-items:center;

    padding:12px 22px;

    border-radius:14px;

    background:#2563eb;

    color:white !important;

    text-decoration:none;

    font-weight:650;

    font-size:14px;

    position:relative;
    z-index:2;
}

.btn:hover{

    background:#3b82f6;
}

/* FOOTER */

.footer{

    margin-top:70px;

    color:#64748b;

    font-size:13px;
}

</style>

<div class="main-wrap">

<div class="hero-title">
TCO Intelligence Platform
</div>

<div class="hero-sub">
Operational analytics platform for lifecycle cost optimization,
maintenance intelligence, rental evaluation, and compressor ownership analysis.
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
Analyze operational cost exposure across fuel consumption,
maintenance quality, downtime, overhaul cycles,
and replacement frequency.
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
Evaluate profitability, utilization efficiency,
ownership recovery, and operating economics
across varying machine conditions.
</div>

<a class="btn" href="?page=rental" target="_self">
Open Tool
</a>

</div>

</div>

<div class="footer">
Chicago Pneumatic • Internal Business Platform
</div>

</div>

""", unsafe_allow_html=True)