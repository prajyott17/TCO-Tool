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
<div class="hero-section">

<div class="hero-small">
WELCOME TO CHICAGO PNEUMATIC
</div>

<div class="hero-main">
Smart Insights. Better Uptime.<br>
<span class="hero-red">
Lower Cost.
</span>
</div>

<div class="hero-desc">
Analyze lifecycle costs, compare genuine vs non-genuine parts,
and optimize rental profitability from a single platform.
</div>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero-buttons">

<a href="?page=tco_genuine"
target="_self"
class="hero-btn-red">
📊 Open TCO Tool
</a>

<a href="?page=rental"
target="_self"
class="hero-btn-outline">
⛽ Open Rental Calculator
</a>

</div>
""", unsafe_allow_html=True)
# ================= SECTION TITLE =================
st.markdown(
    '<div class="section-title">OUR TOOLS</div>',
    unsafe_allow_html=True
)

# ================= 3 CARDS =================

col1, col2, col3 = st.columns([3.5, 3.5, 3])

# ---------- CARD 1 ----------
with col1:
    st.markdown(
    """
    <div class="tco-card">

    <div class="label">
    LIFECYCLE ANALYTICS
    </div>

    <div class="card-title">
    📊 TCO Genuine vs Non-Genuine
    </div>

    <div class="card-desc">
    Compare Total Cost of Ownership between
    Genuine and Non-Genuine parts over the
    machine lifecycle.
    </div>

    <div class="card-feature">✔ Cost Breakdown Comparison</div>
    <div class="card-feature">✔ Savings Analysis</div>
    <div class="card-feature">✔ Detailed Reports</div>

    <div style="height:20px;"></div>

    <a href="?page=tco_genuine"
    target="_self"
    class="card-btn">
    Open TCO Tool →
    </a>

    </div>
    """,
    unsafe_allow_html=True
    )
# ---------- CARD 2 ----------
with col2:

    st.markdown(
    """
    <div class="rental-card">

    <div class="label">
    RENTAL INTELLIGENCE
    </div>

    <div class="card-title">
    📊 Rental Calculator
    </div>

    <div class="card-desc">
    Calculate ownership cost recovery,<br>
    rental rates, utilization and<br>
    profitability analysis.
    </div>

    <div class="card-feature">✔ Break-even Analysis</div>
    <div class="card-feature">✔ Utilization & Revenue</div>
    <div class="card-feature">✔ ROI & Payback Period</div>

    <div style="height:20px;"></div>

    <a href="?page=rental"
    target="_self"
    class="card-btn rental-btn">
    Open Rental Calculator →
    </a>

    </div>
    """,
    unsafe_allow_html=True
    )
# ---------- CARD 3 ----------

with col3:

    st.markdown(
    """
    <div class="benefit-card">

    <div class="label">
    BENEFITS
    </div>

    <div class="card-title">
    ⭐ Why Choose Genuine Parts?
    </div>

    <div class="benefit-item">
        <strong>💰Lower Total Cost</strong>
        <div class="benefit-text">
            Reduced maintenance and operating expenses
        </div>
    </div>

    <div class="benefit-item">
        <strong>⏱  Higher Uptime</strong>
        <div class="benefit-text">
            Fewer breakdowns and better availability
        </div>
    </div>

    <div class="benefit-item">
        <strong>⚙️Longer Machine Life</strong>
        <div class="benefit-text">
            Improved durability and reliability
        </div>
    </div>

    <div class="benefit-item">
        <strong>📈 Better ROI</strong>
        <div class="benefit-text">
            Higher returns over the equipment lifecycle
        </div>
    </div>
    """,
    unsafe_allow_html=True
    )
# ================= FOOTER =================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    '''
    <div class="footer">
        Chicago Pneumatic • Internal Business Platform
    </div>
    ''',
    unsafe_allow_html=True
)