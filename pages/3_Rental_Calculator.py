import streamlit as st
import pandas as pd
from utils import load_css

st.set_page_config(
    page_title="Rental",
    layout="wide",
    initial_sidebar_state="collapsed"
)
load_css()

from nav import top_nav
currency = top_nav("rental")

# ===== Currency Mapping =====
if currency == "INR (₹)":
    symbol = "₹"
    rate = 1
elif currency == "USD ($)":
    symbol = "$"
    rate = 1/93
elif currency == "EURO (€)":
    symbol = "€"
    rate = 1/107

# ================= UI =================

st.markdown("""
<style>
/* ================= COMPACT CLEAN UI ================= */
            
.metric-card {

    background:
        rgba(255,255,255,0.28);

    border:
        1px solid rgba(255,255,255,0.28);

    padding: 12px;

    border-radius: 14px;

    backdrop-filter:
        blur(8px);

    box-shadow:
        0 4px 12px rgba(15,23,42,0.04);

    text-align:center;

    transition:0.2s ease;

    border-top:
        3px solid rgba(216,75,75,0.16);
}
.metric-card:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 14px 28px rgba(15,23,42,0.12);
}

.metric-card div:first-child {
    font-size: 13px;             
    margin-bottom: 2px;
    color:inherit;
    opacity:0.75;
}

.big-number {
    font-size: 18px;          
    font-weight: 600;
}

/* SECTION TITLES */
.section-title {
    font-size: 18px;         
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 4px;
}

/* HIGHLIGHT BOX */
.highlight-box {
    padding: 8px;
    border-radius: 10px;
    margin-top: 8px;
    margin-bottom: 8px;
    font-size: 16px;
}

.highlight-number {
    font-size: 18px;
    font-weight: 600;
}

/* REMOVE EXTRA GAPS */
.element-container {
    margin-bottom: 4px !important;  
}

            /* ================= CENTER ALIGN UI ================= */

/* section titles */
.section-title {
    text-align: center;
}

/* metric cards content */
.metric-card {
    text-align: center;
}

/* highlight box */
.highlight-box {
    text-align: center;
}

/* big numbers center */
.big-number {
    text-align: center;
}

/* Streamlit metric (bottom comparison) */
div[data-testid="stMetric"] {
    text-align: center;
}

/* optional: center headings */
h1, h2, h3 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)
# ================= FUNCTION =================
def safe_float(val):
    try:
        return 0 if pd.isna(val) else float(val)
    except:
        return 0

# ================= LOAD EXCEL =================
@st.cache_data
def load_data():
    df_raw = pd.read_excel("Rental/Rental Customer.xlsx", header=None)

    cols = (
        df_raw.iloc[0].fillna('').astype(str) + " " +
        df_raw.iloc[1].fillna('').astype(str)
    ).str.strip()

    df = df_raw[2:].copy()
    df.columns = cols
    df.reset_index(drop=True, inplace=True)

    return df

if "fuel_df" not in st.session_state:
    st.session_state.fuel_df = load_data()

df = st.session_state.fuel_df

# ================= MACHINE =================
machine_col = [c for c in df.columns if "discrip" in c.lower()][0]
left_panel, divider, right_panel = st.columns([0.65, 0.02, 3.33])
with divider:
    st.markdown("""
    <div class="vertical-divider"></div>
    """, unsafe_allow_html=True)
with left_panel:

    st.markdown("""
    <div class="page-card">
    <h5 style='text-align:center;'>⚙️ Inputs</h5>
    """, unsafe_allow_html=True)

    machine = st.selectbox(
        "Machine",
        df[machine_col].dropna().unique()
    )

    selected_data = df[df[machine_col] == machine].iloc[0]

    price = safe_float(selected_data.iloc[2])
    rental_default = safe_float(selected_data.iloc[3])
    pm_750 = safe_float(selected_data.iloc[10])
    pm_1500 = safe_float(selected_data.iloc[16])

    qty = st.number_input(
        "No. of Machines",
        1,
        100,
        1
    )

    hours = st.slider(
        "Hours",
        0,
        600,
        100
    )

    months = st.slider(
        "Months",
        1,
        12,
        6
    )

    monthly_rent = st.number_input(
        f"Monthly Rental ({symbol})",
        min_value=0,
        value=int(rental_default),
        step=1000
    )

    fuel_consumption = st.number_input(
        "Fuel Consumption (L/hr)",
        1,
        50,
        10
    )

    fuel_price = st.number_input(
        f"Fuel Price ({symbol}/L)",
        50,
        150,
        90
    )

    st.markdown("</div>", unsafe_allow_html=True)
# ================= CALCULATIONS =================
# Investment
investment = price * qty

# Earnings
total_rent = monthly_rent * months
roi_actual = (total_rent/price *100) if price else 0
roi_annual = ((total_rent / price) * (12/months)*100) if price else 0
payback_months = round(price / monthly_rent, 1) if monthly_rent else 0

# Fuel
fuel_per_hr = fuel_consumption * fuel_price
monthly_fuel = fuel_per_hr * hours * qty
total_fuel = monthly_fuel * months

fuel_saving = total_fuel * 0.07
adjusted_fuel = total_fuel - fuel_saving

# Maintenance
total_hours = hours * months

if total_hours < 750:
    maintenance = 0
    msg = "No maintenance savings yet (750 hrs kit not reached)"
elif total_hours < 1500:
    maintenance = pm_750
    msg = "750 hrs Kit Savings"
else:
    maintenance = pm_1500
    msg = "1500 hrs Kit Savings"

# Final
final_cost = adjusted_fuel - maintenance
total_savings = fuel_saving + maintenance
with right_panel:
# ================= UI =================

    st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;'>

    <div style='font-size:27px; font-weight:700;'>
    ⛽ Rental for Diesel Machine
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
            <div style='font-size:15px; color:inherit; opacity:0.75; font-weight:500; margin-bottom:10px;'>
            Estimate savings using genuine parts and maintenance kits
            </div>
            """, unsafe_allow_html=True)
    # Investment
    st.markdown('<div class="section-title">💰 Investment</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    c1.markdown(f"<div class='metric-card'><div>New Machine Price</div><div class='big-number'>{symbol} {price * rate:,.0f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div>Total Price</div><div class='big-number'>{symbol} {investment * rate:,.0f}</div></div>", unsafe_allow_html=True)
    st.divider()

    # Earnings
    st.markdown('<div class="section-title">📈 Earnings</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    # Monthly Rental (keep this)
    c1.markdown(f"""
    <div class='metric-card'>
    <div>Monthly Rental</div>
    <div class='big-number'>{symbol} {monthly_rent * rate:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Total Rental
    c2.markdown(f"""
    <div class='metric-card'>
    <div>Total Rental ({months} months)</div>
    <div class='big-number'>{symbol} {total_rent * rate:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # ROI for selected duration
    c3.markdown(f"""
    <div class='metric-card'>
    <div>ROI ({months} months)</div>
    <div class='big-number'>{roi_actual:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Annual ROI
    c4.markdown(f"""
    <div class='metric-card'>
    <div>Annual ROI</div>
    <div class='big-number'>{roi_annual:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:18px; font-weight:500; margin-top:10px; color:#d84b4b;'>
    💰 You earn <b>{symbol} {total_rent * rate:,.0f}</b> in {months} months
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='metric-card'>
    Payback Period<br>
    <div class='highlight-number'>{payback_months} months</div>
    </div>
    """, unsafe_allow_html=True)
    if payback_months <= months:
        st.markdown(
        "<div style='color:#28a745; font-weight:500;'>💰 Investment can be recovered within selected duration</div>",
        unsafe_allow_html=True
    )
    else:
        st.info("⏳ Full recovery needs more rental months")

    st.divider()

    # Operating Cost
    st.markdown('<div class="section-title">⚙️ Operating Cost</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    c1.markdown(f"<div class='metric-card'><div>Monthly Fuel Cost</div><div class='big-number'>{symbol} {monthly_fuel * rate:,.0f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div>Total Fuel Cost ({months} months)</div><div class='big-number'>{symbol} {total_fuel * rate:,.0f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div>Fuel Saving using Genuine Parts(7%)</div><div class='big-number'>{symbol} {fuel_saving * rate:,.0f}</div></div>", unsafe_allow_html=True)

    # Adjusted Fuel
    st.markdown(f"""
    <div class='metric-card'>
    <div>Fuel Cost After Savings</div>
    <div class='big-number'>{symbol} {adjusted_fuel * rate:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    # ================= PROGRESS BAR =================
    st.markdown("##### 📊 Maintenance Savings Progress")

    progress_value = min(total_hours / 1500, 1.0)
    st.progress(progress_value)

    if total_hours < 750:
        st.caption("You are close to unlocking maintenance savings (750 hours kit)")
    elif total_hours < 1500:
        st.caption("750 hours kit savings active • Higher savings ahead at 1500 hours")
    else:
        st.caption("Full maintenance savings unlocked")

    # Maintenance
    st.markdown('<div class="section-title">🛠️ Maintenance Savings</div>', unsafe_allow_html=True)

    if maintenance == 0:
        st.info(msg)
    else:
        st.markdown(f"<div class='metric-card'><div>{msg}</div><div class='big-number'>{symbol} {maintenance * rate:,.0f}</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    # Final Cost
    c1.markdown(f"""
    <div class='metric-card'>
    <div>Final Cost After Savings</div>
    <div class='big-number'>{symbol} {final_cost * rate:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Total Savings
    c2.markdown(f"""
    <div class='metric-card'>
    <b>Total Savings</b><br>
    <div class='highlight-number'>{symbol} {total_savings * rate:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    # Comparison
    st.markdown("##### 📊 Cost Comparison")

    c1, c2 = st.columns(2)
    c1.metric("Without Genuine Parts", f"{symbol} {total_fuel * rate:,.0f}")
    c2.metric("With Genuine Parts", f"{symbol} {final_cost * rate:,.0f}")

    # Footer
    st.caption("Estimated savings based on usage and genuine parts performance.")
    st.success("💡 Higher usage unlocks greater savings through fuel efficiency and maintenance benefits.")