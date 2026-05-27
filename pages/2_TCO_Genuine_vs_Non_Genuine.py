import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from io import BytesIO
from utils import get_rate

rates = get_rate()

st.set_page_config(page_title="TCO Genuine", layout="wide")
from utils import load_css
load_css()
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
from nav import top_nav
try:
    currency = top_nav("tco_genuine")
except Exception as e:
    st.error(f"Navigation error: {e}")
    currency = "INR (₹)"

# ===== Currency =====
if currency == "INR (₹)":
    symbol, rate = "₹", 1
elif currency == "USD ($)":
    symbol, rate = "$", 1 / rates["USD"]
else:
    symbol, rate = "€", 1 / rates["EUR"]

# ================= LOAD =================
@st.cache_data
def load_data():
    file_path = os.path.join("TCO", "CPPT.xlsx")

    if not os.path.exists(file_path):
        st.error("❌ Data file not found. Please check path.")
        st.stop() 

    df = pd.read_excel(file_path)
    df = df[df["Description"].notna()]
    df.columns = df.columns.str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()
    return df

df = load_data()
COLS = [3,1.2,1.2,1.2]

# ================= HELPERS =================
def comparison_header():

    c1, c2, c3, c4 = st.columns(COLS)

    with c2:
        st.markdown(
            '<div class="compare-pill genuine">Genuine</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="compare-pill ng">Non-Genuine</div>',
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            '<div class="compare-pill customer">Customer</div>',
            unsafe_allow_html=True
        )

def row(label, v1, v2, v3, k1, k2, k3, disable_g=False, disable_ng=False):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(label)

    v1 = c2.number_input(label+"_g", value=float(v1),step=0.5,format="%.1f", key=k1,
                         disabled=disable_g, label_visibility="collapsed")

    v2 = c3.number_input(
        label+"_ng",
        value=float(v2),
        step= 0.5,
        format="%.1f",
        key=k2,
        disabled=disable_ng,
        label_visibility="collapsed"
    )

    v3 = c4.number_input(label+"_c", value=float(v3),step= 0.5,format="%.1f", key=k3,
                         label_visibility="collapsed")

    return v1, v2, v3

def total_row(label, v1, v2, v3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(f"**{label}**")
    c2.markdown(f"{symbol} {v1*rate:,.0f}")
    c3.markdown(f"{symbol} {v2*rate:,.0f}")
    c4.markdown(f"{symbol} {v3*rate:,.0f}")

def highlight_total_row(label, v1, v2, v3):

    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown(
        f'<div class="tco-final-label">{label}</div>',
        unsafe_allow_html=True
    )

    c2.markdown(
        f'<div class="tco-final-value genuine">{symbol} {v1*rate:,.0f}</div>',
        unsafe_allow_html=True
    )

    c3.markdown(
        f'<div class="tco-final-value ng">{symbol} {v2*rate:,.0f}</div>',
        unsafe_allow_html=True
    )

    c4.markdown(
        f'<div class="tco-final-value customer">{symbol} {v3*rate:,.0f}</div>',
        unsafe_allow_html=True
    )
    
def single_row(label, default, key):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(label)

    v1 = c2.number_input(label+"_g", value=default, key=key+"_g", label_visibility="collapsed")
    v2 = c3.number_input(label+"_ng", value=default, key=key+"_ng", label_visibility="collapsed")
    v3 = c4.number_input(label+"_c", value=0, key=key+"_c", label_visibility="collapsed")

    return v1, v2, v3
def on_value_change():
    st.session_state.maintenance_last_input = "value"

    m_g = st.session_state.get("maintenance_genuine", 1)

    if m_g > 0:
        st.session_state.maintenance_ng_percent_input = int(
            (st.session_state.maintenance_ng_value_input / m_g) * 100
        )


def on_percent_change():
    st.session_state.maintenance_last_input = "percent"

    m_g = st.session_state.get("maintenance_genuine", 1)

    st.session_state.maintenance_ng_value_input = int(
        (st.session_state.maintenance_ng_percent_input / 100) * m_g
    )
# ================= MACHINE =================
c1, c2 = st.columns([3,3.63])

c1.markdown("Select Machine Model")

machine1 = c2.selectbox(
    "Machine 1",
    df["Description"],
    label_visibility="collapsed"
)
row1 = df[df["Description"] == machine1]

if not row1.empty and "CLP 2026" in row1.columns:
    price_val = row1["CLP 2026"].values[0]
else:
    price_val = 0
price_val = 0 if pd.isna(price_val) else int(price_val)

# ================= INPUTS =================
comparison_header()
c1, c2, c3, c4 = st.columns(COLS)

c1.markdown("Initial Investment (Machine Cost)")

price_g = c2.number_input(
    "price_g",
    value=int(price_val * rate),
    step=10000,
    key=f"price_g_{machine1}",
    label_visibility="collapsed"
)

price_ng = c3.number_input(
    "price_ng",
    value=int(price_val * rate),
    step=10000,
    key=f"price_ng_{machine1}",
    label_visibility="collapsed"
)

price_c = c4.number_input(
    "price_c",
    value=0,
    step=10000,
    key="price_c",
    label_visibility="collapsed"
)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
# ================= GLOBAL INPUTS =================

col1, col2, col3, col4 = st.columns([3,1.2,1.2,1.2])
col1.markdown("Total Operating Years")
y = col2.number_input("y", value=10, key="y", min_value=1, label_visibility="collapsed")
y_g = y_ng = y_c = y
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
# ================= MAINTENANCE =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Preventive Maintenance Cost**", expanded=False):
    st.caption(
        "Lower preventive maintenance investment may increase fuel consumption, wear, and unexpected failures over time."
    )
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Annual Preventive Maintenance Cost")

    # ===== GENUINE =====
    if "maintenance_ng_value_input" not in st.session_state:
        st.session_state.maintenance_ng_value_input = int(152600)

    if "maintenance_ng_percent_input" not in st.session_state:
        st.session_state.maintenance_ng_percent_input = 70.0
    m_g = c2.number_input(
        "m_g",
        value=218000,
        key="maintenance_genuine",
        label_visibility="collapsed"
    )

    if "maintenance_last_input" not in st.session_state:
        st.session_state.maintenance_last_input = "value"
    # Get current state
    val = st.session_state.maintenance_ng_value_input
    pct = st.session_state.maintenance_ng_percent_input
    last = st.session_state.maintenance_last_input

    
    # ===== SYNC BEFORE WIDGETS =====
    if last == "value":
        val = st.session_state.maintenance_ng_value_input
        if m_g > 0:
            pct = round((st.session_state.maintenance_ng_value_input / m_g) * 100, 2)
            st.session_state.maintenance_ng_percent_input = pct

    elif last == "percent":
        pct = st.session_state.maintenance_ng_percent_input
        val = round((pct / 100) * m_g, 0)
        st.session_state.maintenance_ng_value_input = val


    # ===== NON-GENUINE UI (VALUE + %) =====
    col_ng_val, col_ng_pct = c3.columns([1.66,1.34])

    # VALUE INPUT
    m_ng_val = col_ng_val.number_input(
        "₹",
        key="maintenance_ng_value_input",
        step=1000,
        format="%d",
        on_change=on_value_change,
        label_visibility="collapsed"
    )

    pct_col1, pct_col2 = col_ng_pct.columns([5,1])

    m_ng_pct = pct_col1.number_input(
        "maintenance_pct",
        key="maintenance_ng_percent_input",
        min_value=0.0,
        max_value=100.0,
        on_change=on_percent_change,
        label_visibility="collapsed"
    )

    pct_col2.markdown(
        "<div style='padding-top:6px; font-weight:500; font-size:14px;'>%</div>",
        unsafe_allow_html=True
    )
    
    val = st.session_state.maintenance_ng_value_input
    pct = st.session_state.maintenance_ng_percent_input
    last = st.session_state.maintenance_last_input

    # ===== FINAL VALUES =====
    m_ng = st.session_state.maintenance_ng_value_input

    # ===== CUSTOMER =====
    m_c = c4.number_input("m_c", value=0, label_visibility="collapsed")

    # ===== TOTAL =====
    maint_g = m_g * y
    maint_ng = m_ng * y
    maint_c = m_c * y

    m_ng_pct_final = st.session_state.maintenance_ng_percent_input

    if m_ng_pct_final >= 80:
        risk_level = "🟢 Low Operational Risk"
        fc_multiplier = 1.07
        multiplier = 1.5

    elif m_ng_pct_final >= 60:
        risk_level = "🟠 Moderate Operational Risk"
        fc_multiplier = 1.105
        multiplier = 2.0

    else:
        risk_level = "🔴 High Operational Risk"
        fc_multiplier = 1.14
        multiplier = 3.0
    st.caption(f"Maintenance Quality Assessment: {risk_level}")
    st.caption(
    "Operational impact estimates are dynamically adjusted based on maintenance effectiveness and typical machine operating conditions."
    )
    total_row("Total Preventive Maintenance Cost", maint_g, maint_ng, maint_c)

st.markdown('</div>', unsafe_allow_html=True)
multiplier = multiplier if 'multiplier' in locals() else 1.5
fc_multiplier = fc_multiplier if 'fc_multiplier' in locals() else 1.07

# ================= FUEL COST =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Fuel Cost**", expanded=False):
    st.caption(
        "Poor maintenance can reduce machine efficiency and increase fuel consumption throughout machine life."
    )
    col1, col2 = st.columns([3,3.63])
    col1.markdown("Fuel Price per Liter")
    fp = col2.number_input("fp", value=93, key="fp", label_visibility="collapsed")

    fp_g = fp_ng = fp_c = fp

    col1, col2 = st.columns([3,3.63])
    col1.markdown("Operating Hours per Year")
    h = col2.number_input("h", value=2000, key="h", label_visibility="collapsed")
    h_g = h_ng = h_c = h

# ================= FUEL INPUT =================
    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown("Fuel Consumption per Hour (Liters)")

    fc_g = c2.number_input("fc_g", value=65, key="fc_g", label_visibility="collapsed")

    fc_ng = fc_g * fc_multiplier

    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{round(fc_ng, 2)}</span>
            <span style="font-size:11px; color:#64748b;">↑{(fc_multiplier - 1)*100:.1f}%</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    fc_c = c4.number_input("fc_c", value=0, key="fc_c", label_visibility="collapsed")

# ================= TOTALS =================

    fuel_g = fp_g * fc_g * h_g * y_g
    fuel_ng = fp_ng * fc_ng * h_ng * y_ng
    fuel_c = fp_c * fc_c * h_c * y_c

    total_row("Total Fuel Cost", fuel_g, fuel_ng, fuel_c)
st.markdown('</div>', unsafe_allow_html=True)

# ================= O/H =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Major Overhaul Cost**", expanded=False):
    st.caption(
        "Insufficient maintenance can accelerate component wear and increase overhaul expenses."
    )

    condition_not_met = ((h_g * y_g) < 7500) or (y_g < 6)

    e_g_default = 700000
    c_g_default = 500000
    a_g_default = 200000

    # ===== ENGINE =====
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Engine Overhaul Cost")

    # ✅ Genuine ALWAYS editable
    e_g = c2.number_input("e_g", value=e_g_default, key="e_g", label_visibility="collapsed")

    # ❌ Non-genuine NEVER input → always derived
    e_ng = int(e_g * multiplier)

    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{e_ng:,}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    e_c = c4.number_input("e_c", value=0, key="e_c", label_visibility="collapsed")

    # ===== ELEMENT =====
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Element Overhaul Cost")

    c_g = c2.number_input("c_g", value=c_g_default, key="c_g", label_visibility="collapsed")

    c_ng = int(c_g * multiplier)

    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{c_ng:,}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_c = c4.number_input("c_c", value=0, key="c_c", label_visibility="collapsed")
    # ===== ADD-ON =====
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Add-Hoc Cost")

    # Genuine input
    a_g = c2.number_input("a_g", value=a_g_default, key="a_g", label_visibility="collapsed")

    # Derived NG
    a_ng = int(a_g * multiplier)

    # Display NG (same UI)
    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{a_ng:,}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Customer input
    a_c = c4.number_input("a_c", value=0, key="a_c", label_visibility="collapsed")
    # ===== TOTAL LOGIC =====

    if condition_not_met:
        oh_g = 0
    else:
        oh_g = e_g + c_g + a_g

    oh_ng = e_ng + c_ng + a_ng
    oh_c = e_c + c_c + a_c

    total_row("Total Overhaul Cost", oh_g, oh_ng, oh_c)

st.markdown('</div>', unsafe_allow_html=True)
# ================Downtime==============
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Downtime Cost**", expanded=False):
    st.caption(
        "Downtime impacts productivity, labor utilization, project schedules, and business revenue."
    )
    c1, _, _, _ = st.columns(COLS)
    inc_g, inc_ng, inc_c = single_row("Revenue Loss per Hour", 5000, "inc")
    lab_g, lab_ng, lab_c = single_row("Idle Labor Cost per Hour", 1000, "lab")
    pen_g, pen_ng, pen_c = row("Penalty Cost per Hour", 500, 500, 0, "pen_g","pen_ng","pen_c", disable_ng=False)
    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown("Downtime Hours per Year")

    d_g = c2.number_input("d_g", value=100, key="d_g", label_visibility="collapsed")
    d_ng = int(d_g * multiplier)

    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{d_ng}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    d_c = c4.number_input("d_c", value=0, key="d_c", label_visibility="collapsed")
    down_g = (inc_g + lab_g + pen_g) * d_g * y_g
    down_ng = (inc_ng + lab_ng + pen_ng) * d_ng * y_ng
    down_c = (inc_c + lab_c + pen_c) * d_c * y_c

    total_row("Total Downtime Impact", down_g, down_ng, down_c)

st.markdown('</div>', unsafe_allow_html=True)

# =================Breakdown================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Breakdown Repair Cost**", expanded=False):
    st.caption(
        "Unexpected failures may result in emergency repair costs and operational disruptions."
    )
    c1, _, _, _ = st.columns(COLS)

    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown("Breakdown Repair Cost per Event")

    b_g = c2.number_input("b_g", value=300000, key="b_g", label_visibility="collapsed")

    # Derived NG value
    b_ng = int(b_g * multiplier)

    # Customer input stays editable
    b_c = c4.number_input("b_c", value=0, key="b_c", label_visibility="collapsed")

    # Display NG (not input)
    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{b_ng:,}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    f_g, f_ng, f_c = row("Breakdowns per Year", 1, 2, 0, "f_g","f_ng","f_c")
    break_g = b_g * f_g * y_g
    break_ng = b_ng * f_ng * y_ng 
    break_c = b_c * f_c * y_c

    total_row("Total Breakdown Cost", break_g, break_ng, break_c)   

st.markdown('</div>', unsafe_allow_html=True)

# ============ Replacement Cost===============
st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("**Machine Replacement Cost**", expanded=False):
    st.caption(
        "Poor maintenance practices may increase the frequency of major component replacements."
    )
    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown("Replacement Cost per Event")

    rep_cost_g = c2.number_input("rep_cost_g", value=200000, key="rep_cost_g", label_visibility="collapsed")

    # Derived NG value
    rep_cost_ng = int(rep_cost_g * multiplier)

    # Customer input stays editable
    rep_cost_c = c4.number_input("rep_cost_c", value=0, key="rep_cost_c", label_visibility="collapsed")

    # Display NG (not input)
    c3.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            border:1px solid #dbe2ea;
            border-radius:6px;
            padding:6px 8px;
            background:#f8fafc;
            font-size:14px;
        ">
            <span>{rep_cost_ng:,}</span>
            <span style="font-size:11px; color:#64748b;">×{multiplier}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    rep_freq_g, rep_freq_ng, rep_freq_c = row("Replacements per Year", 1, 2, 0, "rep_freq_g", "rep_freq_ng","rep_freq_c")
    rep_g = rep_cost_g * rep_freq_g * y_g
    rep_ng = rep_cost_ng * rep_freq_ng * y_ng
    rep_c = rep_cost_c * rep_freq_c * y_c

    total_row("Total Replacement Cost", rep_g, rep_ng, rep_c)

st.markdown('</div>', unsafe_allow_html=True)
if st.button("Calculate TCO"):
    st.session_state.calculated = True
if st.session_state.get("calculated", False):

    with st.container(border=True):
        st.markdown(
    """
    <style>

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-hook) {

        border-radius: 24px !important;

        border: 1px solid #dbe7f3 !important;

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06),
            0 2px 8px rgba(15,23,42,0.04) !important;

        overflow: visible;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-hook) > div {

        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f8fbff 100%
        ) !important;

        padding: 28px !important;

        border-radius: 24px !important;
    }

    .result-hook {
        display:none;
    }

    </style>

    <div class="result-hook"></div>
    """,
    unsafe_allow_html=True
)

            # ALL RESULT CODE HERE
        tco_g = price_g + fuel_g + maint_g + oh_g + down_g + break_g + rep_g
        tco_ng = price_ng + fuel_ng + maint_ng + oh_ng + down_ng + break_ng + rep_ng
        fuel_saving = fuel_ng - fuel_g
        oh_saving = oh_ng - oh_g
        breakdown_saving = break_ng - break_g
        replacement_saving = rep_ng - rep_g
        saving_percent = 0
        if tco_ng > 0:
            saving_percent = ((tco_ng - tco_g) / tco_ng) * 100


    # ================= RESULT =================
        st.markdown("#### Total Cost of Ownership")

        comparison_header()
        tco_c = price_c + fuel_c + maint_c + oh_c + down_c + break_c + rep_c

        highlight_total_row(
            f"Total Cost of Ownership ({y} Years)",
            tco_g,
            tco_ng,
            tco_c
        )
        st.markdown("---")
        # ================= TOTAL SAVINGS =================
        # Calculate savings
        total_saving_value = tco_ng - tco_g

        if tco_ng > 0:
            total_saving_pct = (total_saving_value / tco_ng) * 100
        else:
            total_saving_pct = 0

        # Color logic
        color = "green" if total_saving_value > 0 else "red"

        c1, c2, c3 = st.columns([2,2,3])
        with c1:
            st.metric(
            label="💰 Total Savings",
            value=f"{symbol} {total_saving_value*rate:,.0f}",
            delta=f"{total_saving_pct:.1f}%"
        )
        if total_saving_value > 0:
            st.success(f"You save {symbol} {total_saving_value*rate:,.0f} by choosing Genuine")
        else:
            st.error("No savings with Genuine option")

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(COLS)
        c1.markdown("Total Savings Percentage")
        color = "green" if saving_percent > 0 else "red"
        c2.markdown(f"<span style='color:{color}; font-weight:600'>{saving_percent:.1f}%</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("###### Savings with Genuine")
        c1, c2, c3, c4 = st.columns(COLS)
        fuel_pct = (fuel_saving / fuel_ng * 100) if fuel_ng > 0 else 0
        c1.markdown(
            '<div class="saving-label">Fuel Cost Savings</div>',
            unsafe_allow_html=True
        )

        fuel_color = "saving-negative" if fuel_saving < 0 else "saving-value"

        c2.markdown(
            f'<div class="{fuel_color}">{symbol} {fuel_saving * rate:,.0f} <span class="saving-percent">({fuel_pct:.1f}%)</span></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(COLS)
        base_oh_ng = oh_ng
        oh_pct = (oh_saving / base_oh_ng * 100) if base_oh_ng > 0 else 0
        c1.markdown(
            '<div class="saving-label">Overhaul Cost Savings</div>',
            unsafe_allow_html=True
        )

        oh_color = "saving-negative" if oh_saving < 0 else "saving-value"

        c2.markdown(
            f'<div class="{oh_color}">{symbol} {oh_saving * rate:,.0f} <span class="saving-percent">({oh_pct:.1f}%)</span></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(COLS)
        break_pct = (breakdown_saving / break_ng * 100) if break_ng > 0 else 0
        c1.markdown(
            '<div class="saving-label">Breakdown Cost Savings</div>',
            unsafe_allow_html=True
        )

        break_color = "saving-negative" if breakdown_saving < 0 else "saving-value"

        c2.markdown(
            f'<div class="{break_color}">{symbol} {breakdown_saving * rate:,.0f} <span class="saving-percent">({break_pct:.1f}%)</span></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(COLS)
        rep_pct = (replacement_saving / rep_ng * 100) if rep_ng > 0 else 0
        c1.markdown(
            '<div class="saving-label">Replacement Cost Savings</div>',
            unsafe_allow_html=True
        )

        rep_color = "saving-negative" if replacement_saving < 0 else "saving-value"

        c2.markdown(
            f'<div class="{rep_color}">{symbol} {replacement_saving * rate:,.0f} <span class="saving-percent">({rep_pct:.1f}%)</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown(
            """
            <div class="results-section-title">
                Cost Breakdown Comparison
            </div>
            """,
            unsafe_allow_html=True
        )

        labels = ["Investment", "Fuel", "Maintenance", "O/H", "Downtime", "Breakdown", "Replacement"]

        values_g = [price_g, fuel_g, maint_g, oh_g, down_g, break_g, rep_g]
        values_ng = [price_ng, fuel_ng, maint_ng, oh_ng, down_ng, break_ng, rep_ng]
        values_c = [price_c, fuel_c, maint_c, oh_c, down_c, break_c, rep_c]
        col1, col2, col3 = st.columns(3)

        def donut_chart_plotly(values, labels, title, total):

            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.70,
                sort=False,
                hoverinfo='label+percent+value',
                marker=dict(colors = [
                        "#000000",
                        [
                        "#1f2937",
                        "#d84b4b",
                        "#ef4444",
                        "#f59e0b",
                        "#10b981",
                        "#6b7280"
                        ]
                        ]),
                textinfo='none' 
            )])

            fig.update_layout(
                height=250,
                margin=dict(t=15, b=5, l=5, r=5),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                autosize=True,
                annotations=[
                    dict(
                        text=f"{title}<br><b>{symbol} {total*rate:,.0f}</b>",
                        x=0.5, y=0.5,
                        font_size=14,
                        showarrow=False
                    )
                ]
            )
            return fig
        total_g = sum(values_g)

        chart_colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]

        with col1:
            st.plotly_chart(
                donut_chart_plotly(values_g, labels, "Genuine", tco_g),
                width="content",
                config={"displayModeBar": False}
            )
        with col2:
            st.plotly_chart(
                donut_chart_plotly(values_ng, labels, "Non-Genuine", tco_ng),
                width="content",
                config={"displayModeBar": False}
            )
        with col3:
            st.plotly_chart(
                donut_chart_plotly(values_c, labels, "Customer", tco_c),
                width="content",
                config={"displayModeBar": False}
            )
        st.markdown(
            """
            <div style='text-align:center; font-size:12px;'>
            <span style='color:#4E79A7;'>●</span> Fuel &nbsp;&nbsp;
            <span style='color:#F28E2B;'>●</span> Maintenance &nbsp;&nbsp;
            <span style='color:#E15759;'>●</span> O/H &nbsp;&nbsp;
            <span style='color:#76B7B2;'>●</span> Downtime &nbsp;&nbsp;
            <span style='color:#59A14F;'>●</span> Breakdown &nbsp;&nbsp;
            <span style='color:#EDC948;'>●</span> Replacement &nbsp;&nbsp;
            <span style='color:#000000;'>●</span> Investment &nbsp;&nbsp;
            </div>
            """,
            unsafe_allow_html=True
    )
        
        st.markdown("##### 📊 Savings Contribution by Category")

        saving_components = ["Fuel", "Overhaul", "Breakdown", "Replacement"]
        savings = [fuel_saving, oh_saving, breakdown_saving, replacement_saving]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=saving_components,
            y=savings,

            text=[f"{symbol} {s*rate:,.0f}" for s in savings],

            textposition='outside',

            marker=dict(
                color=[
                "#d84b4b",
                "#10b981",
                "#f59e0b",
                "#6b7280"
                ]
            ),

            hovertemplate=
                "<b>%{x}</b><br>" +
                f"{symbol} %{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(

            height=360,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            margin=dict(
                t=30,
                b=20,
                l=10,
                r=10
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="#e2e8f0",
                zeroline=False
            ),

            xaxis=dict(
                showgrid=False
            ),

            font=dict(
                size=13,
                color="#0f172a"
            )
        )
        st.plotly_chart(fig, width="stretch")
        st.markdown("---")

        if st.button("📄 Generate PDF Report"):

            buffer = BytesIO()

            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=20,
                leftMargin=20,
                topMargin=20,
                bottomMargin=18,
            )

            styles = getSampleStyleSheet()
            elements = []

            # ===== TITLE =====
            title = Paragraph(
                f"""
                <para align="center">
                <font size="24"><b>Total Cost of Ownership Report</b></font><br/>
                <font size="11" color="#64748b">
                Genuine vs Non-Genuine vs Customer Scenario
                </font>
                </para>
                """,
                styles['Title']
            )

            elements.append(title)
            elements.append(Spacer(1, 20))
            summary_data = [[
                Paragraph(
                    f"""
                    <font size="16"><b>Total Savings with Genuine</b></font><br/><br/>

                    <font size="24" color="#15803d">
                    <b>{symbol} {total_saving_value*rate:,.0f}</b>
                    </font><br/><br/>

                    Savings Percentage:
                    <b>{total_saving_pct:.1f}%</b><br/><br/>

                    Risk Profile:
                    <b>{risk_level}</b>
                    """, 
                    styles['BodyText']
                )
            ]]

            summary_table = Table(summary_data, colWidths=[520])

            summary_table.setStyle(TableStyle([

                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),

                ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#cbd5e1")),

                ('ROUNDEDCORNERS', [12,12,12,12]),

                ('LEFTPADDING', (0,0), (-1,-1), 20),
                ('RIGHTPADDING', (0,0), (-1,-1), 20),

                ('TOPPADDING', (0,0), (-1,-1), 18),
                ('BOTTOMPADDING', (0,0), (-1,-1), 18),
            ]))

            elements.append(summary_table)

            elements.append(Spacer(1, 24))
            # ===== INPUT SUMMARY =====

            elements.append(
                Paragraph(
                    "<b>Input Parameters</b>",
                    styles['Heading2']
                )
            )

            input_data = [
                ["Parameter", "Value"],

                ["Machine Model", machine1],
                ["Operating Years", str(y)],
                ["Fuel Price per Liter", f"{symbol} {fp}"],
                ["Operating Hours per Year", f"{h:,}"],

                ["Fuel Consumption per Hour", f"{fc_g} L/hr"],

                ["Maintenance Risk Level", risk_level],
            ]

            input_table = Table(input_data, colWidths=[250,250])

            input_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dbeafe")),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
                ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ]))

            elements.append(input_table)
            elements.append(Spacer(1, 20))
            # ===== MACHINE =====
            elements.append(
                Paragraph(
                    f"<b>Machine Model:</b> {machine1}",
                    styles['BodyText']
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Total Operating Years:</b> {y}",
                    styles['BodyText']
                )
            )

            elements.append(Spacer(1, 20))

            # ===== TABLE =====
            data = [
                ["Category", "Genuine", "Non-Genuine", "Customer"],

                ["Initial Investment",
                f"{symbol} {price_g*rate:,.0f}",
                f"{symbol} {price_ng*rate:,.0f}",
                f"{symbol} {price_c*rate:,.0f}"],

                ["Fuel Cost",
                f"{symbol} {fuel_g*rate:,.0f}",
                f"{symbol} {fuel_ng*rate:,.0f}",
                f"{symbol} {fuel_c*rate:,.0f}"],

                ["Preventive Maintenance",
                f"{symbol} {maint_g*rate:,.0f}",
                f"{symbol} {maint_ng*rate:,.0f}",
                f"{symbol} {maint_c*rate:,.0f}"],

                ["Overhaul Cost",
                f"{symbol} {oh_g*rate:,.0f}",
                f"{symbol} {oh_ng*rate:,.0f}",
                f"{symbol} {oh_c*rate:,.0f}"],

                ["Downtime Cost",
                f"{symbol} {down_g*rate:,.0f}",
                f"{symbol} {down_ng*rate:,.0f}",
                f"{symbol} {down_c*rate:,.0f}"],

                ["Breakdown Cost",
                f"{symbol} {break_g*rate:,.0f}",
                f"{symbol} {break_ng*rate:,.0f}",
                f"{symbol} {break_c*rate:,.0f}"],

                ["Replacement Cost",
                f"{symbol} {rep_g*rate:,.0f}",
                f"{symbol} {rep_ng*rate:,.0f}",
                f"{symbol} {rep_c*rate:,.0f}"],

                ["TOTAL TCO",
                f"{symbol} {tco_g*rate:,.0f}",
                f"{symbol} {tco_ng*rate:,.0f}",
                f"{symbol} {tco_c*rate:,.0f}"],
            ]

            table = Table(
                data,
                colWidths=[180, 110, 110, 110]
            )

            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dbeafe")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),

                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

                ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),

                ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

                ('BOTTOMPADDING', (0,0), (-1,0), 10),

                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))

            elements.append(table)

            elements.append(Spacer(1, 20))

            # ===== SAVINGS =====
            savings_para = Paragraph(
                f"""
                <b>Total Savings with Genuine:</b><br/>
                {symbol} {total_saving_value*rate:,.0f}<br/>
                Savings Percentage: {total_saving_pct:.1f}%
                """,
                styles['Heading2']
            )

            elements.append(savings_para)
            elements.append(Spacer(1, 20))

            # ===== EXECUTIVE SUMMARY =====

            elements.append(
                Paragraph(
                    "<b>Executive Summary</b>",
                    styles['Heading2']
                )
            )

            summary_text = f"""
            The Total Cost of Ownership analysis indicates that the Genuine maintenance strategy
            results in overall savings of {symbol} {total_saving_value*rate:,.0f}
            over {y} years compared to the Non-Genuine scenario.

            The savings contribution is primarily driven by:

            • Lower fuel consumption<br/>
            • Reduced overhaul frequency<br/>
            • Lower breakdown occurrence<br/>
            • Reduced replacement cost impact<br/>
            • Lower operational downtime

            The maintenance risk profile for the selected operating conditions is:
            <b>{risk_level}</b>.
            """

            elements.append(
                Paragraph(summary_text, styles['BodyText'])
            )
            elements.append(Spacer(1, 20))

            elements.append(
                Paragraph(
                    "<b>Savings Breakdown</b>",
                    styles['Heading2']
                )
            )

            saving_data = [
                ["Category", "Savings"],

                ["Fuel Savings", f"{symbol} {fuel_saving*rate:,.0f}"],
                ["Overhaul Savings", f"{symbol} {oh_saving*rate:,.0f}"],
                ["Breakdown Savings", f"{symbol} {breakdown_saving*rate:,.0f}"],
                ["Replacement Savings", f"{symbol} {replacement_saving*rate:,.0f}"],
            ]

            saving_table = Table(saving_data, colWidths=[250,250])

            saving_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dcfce7")),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
                ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ]))

            elements.append(saving_table)
            # ===== BUILD =====
            doc.build(elements)

            pdf = buffer.getvalue()
            buffer.close()

            st.download_button(
                label="⬇ Download PDF",
                data=pdf,
                file_name="TCO_Report.pdf",
                mime="application/pdf"
            )