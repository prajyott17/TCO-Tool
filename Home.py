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

<div class="hero">

<div class="section-title">
Available Tools
</div>

<div class="tools-section">

    <div class="tool-card">

        <img src="assets/tool_machine.jpg">

        <h3>TCO Genuine vs Non-Genuine</h3>

        <p>
        Compare lifecycle ownership costs,
        downtime exposure and maintenance.
        </p>

        <a href="?page=tco_genuine"
           target="_self"
           class="btn">
           Open Tool
        </a>

    </div>

    <div class="tool-card">

        <img src="assets/tool_machine.jpg">

        <h3>Rental Calculator</h3>

        <p>
        Evaluate profitability,
        utilization and ROI.
        </p>

        <a href="?page=rental"
           target="_self"
           class="btn">
           Open Tool
        </a>

    </div>

    <div class="benefits-card">

        <h3>
        WHY CHOOSE GENUINE PARTS?
        </h3>

        ✓ Lower Total Cost<br><br>

        ✓ Higher Uptime<br><br>

        ✓ Longer Machine Life<br><br>

        ✓ Better ROI

    </div>

</div>

<div class="footer">

People. Passion. Performance.

<br><br>

© 2026 Chicago Pneumatic

</div>

""", unsafe_allow_html=True)