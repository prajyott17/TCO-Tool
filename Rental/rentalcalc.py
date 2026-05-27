import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# ================= PAGE =================
st.set_page_config(page_title="Fuel Saving Calculator", layout="wide")

# ================= UI =================
st.markdown("""
<style>

.metric-card {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
}
.metric-card:hover {
    transform: translateY(-2px);
    transition: 0.2s ease;
    box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
}
.metric-card div:first-child {
    font-size: 14px;
    color: #4b5563;
    margin-bottom: 4px;
}

.big-number {
    font-size: 22px;
    font-weight: 600;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
}

.highlight-box {
    background-color: rgba(40, 167, 69, 0.12);
    padding: 10px;
    border-radius: 14px;
    border: 1px solid #28a745;
    text-align:center;
    margin-top: 15px;
    margin-bottom: 15px;
    font-size: 18px;            
}

.highlight-number {
    font-size: 20px;
    font-weight: 650;
}

/* Container */
[data-testid="stAppViewContainer"] .block-container {
    max-width: 1100px;
    padding: 20px;
    margin-top: 60px;
    margin-left: 10px;
    margin-right: auto;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
}
section[data-testid="stSidebar"] {
    padding-top: 20px;
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
    df_raw = pd.read_excel("Rental Customer.xlsx", header=None)

    cols = (
        df_raw.iloc[0].fillna('').astype(str) + " " +
        df_raw.iloc[1].fillna('').astype(str)
    ).str.strip()

    df = df_raw[2:].copy()
    df.columns = cols
    df.reset_index(drop=True, inplace=True)

    return df

df = load_data()

# ================= MACHINE =================
machine_col = [c for c in df.columns if "discrip" in c.lower()][0]

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Inputs")

machine = st.sidebar.selectbox("Select Machine", df[machine_col].dropna().unique())

# ================= DATA =================
selected_data = df[df[machine_col] == machine].iloc[0]

price = safe_float(selected_data.iloc[2])
rental_default = safe_float(selected_data.iloc[3])

pm_750 = safe_float(selected_data.iloc[10])
pm_1500 = safe_float(selected_data.iloc[16])
# ================= REST OF SIDEBAR =================

qty = st.sidebar.number_input("No. of Machines", 1, 100, 1)

hours = st.sidebar.slider("Monthly Machine Usage", 0, 600, 100)
monthly_rent = st.sidebar.number_input(
    "Monthly Rental (₹)",
    min_value=0,
    value=int(rental_default),
    step=1000
)
st.sidebar.caption("💡 Default value is from system. Adjust based on region.")
months = st.sidebar.slider("Rental Duration (Months)", 1,12,6)
fuel_consumption = st.sidebar.number_input("Fuel Consumption (L/hr)", 1, 50, 10)
fuel_price = st.sidebar.number_input("Fuel Price (₹/L)", 50, 150, 90)

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

# ================= UI =================

st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;'>

<div style='font-size:27px; font-weight:700;'>
⛽ Fuel Saving and ROI Calculator
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
        <div style='font-size: 15px; color: #6c757d; font-weight:500; margin-bottom:10px;'>
        Estimate savings using genuine parts and maintenance kits
        </div>
        """, unsafe_allow_html=True)
# Investment
st.markdown('<div class="section-title">💰 Investment</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

c1.markdown(f"<div class='metric-card'><div>New Machine Price</div><div class='big-number'>₹ {price:,.0f}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div>Total Price</div><div class='big-number'>₹ {investment:,.0f}</div></div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# Earnings
st.markdown('<div class="section-title">📈 Earnings</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

# Monthly Rental (keep this)
c1.markdown(f"""
<div class='metric-card'>
<div>Monthly Rental</div>
<div class='big-number'>₹ {monthly_rent:,.0f}</div>
</div>
""", unsafe_allow_html=True)

# Total Rental
c2.markdown(f"""
<div class='metric-card'>
<div>Total Rental ({months} months)</div>
<div class='big-number'>₹ {total_rent:,.0f}</div>
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
<div style='font-size:18px; font-weight:500; margin-top:10px; color:#28a745;'>
💰 You earn <b>₹ {total_rent:,.0f}</b> in {months} months
</div>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class='highlight-box'>
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

c1.markdown(f"<div class='metric-card'><div>Monthly Fuel Cost</div><div class='big-number'>₹ {monthly_fuel:,.0f}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div>Total Fuel Cost ({months} months)</div><div class='big-number'>₹ {total_fuel:,.0f}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><div>Fuel Saving using Genuine Parts(7%)</div><div class='big-number'>₹ {fuel_saving:,.0f}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# Adjusted Fuel
st.markdown(f"""
<div class='metric-card'>
<div>Fuel Cost After Savings</div>
<div class='big-number'>₹ {adjusted_fuel:,.0f}</div>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# ================= PROGRESS BAR =================
st.markdown("#### 📊 Maintenance Savings Progress")

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
    st.markdown(f"<div class='metric-card'><div>{msg}</div><div class='big-number'>₹ {maintenance:,.0f}</div></div>", unsafe_allow_html=True)

# Final Cost
st.markdown(f"""
<div class='metric-card'>
<div>Final Cost After Savings</div>
<div class='big-number'>₹ {final_cost:,.0f}</div>
</div>
""", unsafe_allow_html=True)

# Total Savings
st.markdown(f"""
<div class='highlight-box'>
<b>Total Savings</b><br>
<div class='highlight-number'>₹ {total_savings:,.0f}</div>
</div>
""", unsafe_allow_html=True)
st.divider()
# Comparison
st.markdown("### 📊 Cost Comparison")

c1, c2 = st.columns(2)
c1.metric("Without Genuine Parts", f"₹ {total_fuel:,.0f}")
c2.metric("With Genuine Parts", f"₹ {final_cost:,.0f}")

# Footer
st.caption("Estimated savings based on usage and genuine parts performance.")
st.success("💡 Higher usage unlocks greater savings through fuel efficiency and maintenance benefits.")