import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(page_title="TCO Tool", layout="wide")
from utils import load_css
load_css()
from nav import top_nav

currency = top_nav("tco")

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

# ================= LOAD =================
@st.cache_data
def load_data():
    df = pd.read_excel("TCO/CPPT.xlsx", sheet_name=0)
    df = df[df["Description"].notna()]
    df.columns = df.columns.str.strip()

    df["Competitor(Machine 2)"] = df["Competitor(Machine 2)"].astype(str).str.strip().str.lower()
    df["Machine 3"] = df["Machine 3"].astype(str).str.strip().str.lower()
    df["Description"] = df["Description"].astype(str).str.strip()

    return df

df = load_data()
df_display = df.copy()

@st.cache_data
def get_machine_data(df, machine1):
    return df[df["Description"] == machine1]

df_display["Competitor(Machine 2)"] = df_display["Competitor(Machine 2)"].astype(str).str.strip()
df_display["Machine 3"] = df_display["Machine 3"].astype(str).str.strip()

result_container = st.container()
COLS = [2,1,1,1]

# ================= MACHINE =================
c0, c1, c2, c3 = st.columns(COLS)
c0.markdown("Machine Selection")

machine1 = c1.selectbox("Machine 1", df_display["Description"])
row1 = get_machine_data(df, machine1)

price_val = row1["CLP 2026"].values[0] if not row1.empty else 0
new_price1 = 0 if pd.isna(price_val) else int(price_val)

if "price1_input" not in st.session_state or st.session_state.price1_input != new_price1:
    st.session_state.price1_input = new_price1

machine2_list = df_display[df_display["Description"] == machine1]["Competitor(Machine 2)"].dropna().unique().tolist()
machine2 = c2.selectbox("Machine 2", machine2_list)

machine3_list = df_display[df_display["Description"] == machine1]["Machine 3"].dropna().unique().tolist()
machine3 = c3.selectbox("Machine 3", machine3_list)

st.markdown("---")

machine2_clean = str(machine2).strip().lower()
machine3_clean = str(machine3).strip().lower()

# ================= PRICE =================
row2 = df.loc[df["Competitor(Machine 2)"] == machine2_clean].head(1)
price2_val = 0 if row2.empty or pd.isna(row2["Machine 2 Price"].values[0]) else int(row2["Machine 2 Price"].values[0])

row3 = df.loc[df["Machine 3"] == machine3_clean].head(1)
price3_val = 0 if row3.empty or pd.isna(row3["Machine 3 Price"].values[0]) else int(row3["Machine 3 Price"].values[0])

# ================= UI =================
def header():
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("**Parameter**")
    c2.markdown("**Machine 1**")
    c3.markdown("**Machine 2**")
    c4.markdown("**Machine 3**")

def row(label, v1, v2, v3, k1, k2, k3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(label)

    v1 = c2.number_input(f"{label}_m1", value=v1, key=k1, label_visibility="collapsed")
    v2 = c3.number_input(f"{label}_m2", value=v2, key=k2, label_visibility="collapsed")
    v3 = c4.number_input(f"{label}_m3", value=v3, key=k3, label_visibility="collapsed")

    return v1, v2, v3

def total_row(label, v1, v2, v3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(f"**{label}**")
    c2.markdown(f"{symbol} {v1 * rate:,.0f}")
    c3.markdown(f"{symbol} {v2 * rate:,.0f}")
    c4.markdown(f"{symbol} {v3 * rate:,.0f}")

header()

# ================= INITIAL COST =================
c1, c2, c3, c4 = st.columns(COLS)
c1.markdown("Initial Cost")

price1 = c2.number_input("Machine 1 Price", key="price1_input", disabled=True, label_visibility="collapsed",step=1,format="%d")

if "price2_input" not in st.session_state:
    st.session_state.price2_input = price2_val
if "last_machine2" not in st.session_state:
    st.session_state.last_machine2 = machine2_clean
if machine2_clean != st.session_state.last_machine2:
    st.session_state.price2_input = price2_val
    st.session_state.last_machine2 = machine2_clean

price2 = c3.number_input("Machine 2 Price", key="price2_input", label_visibility="collapsed",step=1,format="%d")

if "price3_input" not in st.session_state:
    st.session_state.price3_input = price3_val
if "last_machine3" not in st.session_state:
    st.session_state.last_machine3 = machine3_clean
if machine3_clean != st.session_state.last_machine3:
    st.session_state.price3_input = price3_val
    st.session_state.last_machine3 = machine3_clean

price3 = c4.number_input("Machine 3 Price", key="price3_input", label_visibility="collapsed",step=1,format="%d")

st.markdown("---")

def single_row(label, default, key):
    # Create full row
    c1, c2 = st.columns([2, 3])   # 2 = Parameter, 3 = M1+M2+M3

    # Label (perfectly aligned)
    c1.markdown(label)

    # Input spans across Machine columns
    val = c2.number_input(
        label,
        value=default,
        key=key,
        label_visibility="collapsed"
    )

    return val, val, val
# ================= FUEL =================
c1, _, _, _ = st.columns(COLS)
c1.markdown("**Fuel Cost**")

fp1, fp2, fp3 = single_row("Fuel Cost/L", 93, "fp")
h1, h2, h3 = single_row("Running Hours/year", 2000, "h")
y1, y2, y3 = single_row("Total Years", 10, "y")
fc1, fc2, fc3 = row("Fuel Consumption/Hr", 65, 70, 0, "fc1","fc2","fc3")

fuel1 = fp1 * fc1 * h1 * y1
fuel2 = fp2 * fc2 * h2 * y2
fuel3 = fp3 * fc3 * h3 * y3

total_row("Fuel Cost (Total)", fuel1, fuel2, fuel3)
st.markdown("---")

# ================= MAINTENANCE =================
c1, _, _, _ = st.columns(COLS)
c1.markdown("**Maintenance Cost**")
c1, c2, c3, c4 = st.columns(COLS)

c1.markdown("Maintenance / Year")

m1 = c2.number_input("Machine 1 Maint", value=218000, key="m1", label_visibility="collapsed")
m2 = c3.number_input("Machine 2 Maint", value=109000, key="m2", label_visibility="collapsed")
m3 = c4.number_input("Machine 3 Maint", value=0, key="m3", label_visibility="collapsed")

maint1 = m1 * y1
maint2 = m2 * y2
maint3 = m3 * y3

total_row("Maintenance Cost (Total)", maint1, maint2, maint3)
st.markdown("---")

# ================= O/H =================
c1, c2, _, _ = st.columns(COLS)
c1.markdown("**Major O/H Cost**")

parts = c2.radio("Parts Type", ["Genuine", "Non-Genuine"], horizontal=True, label_visibility="collapsed")

disable_m1_oh = parts == "Genuine" and ((y1 < 6) and (h1 < 7500))

def oh_row(label, v1, v2, v3, k1, k2, k3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(label)

    v1 = c2.number_input(f"{label}_m1", value=v1, key=k1, label_visibility="collapsed", disabled=disable_m1_oh)
    v2 = c3.number_input(f"{label}_m2", value=v2, key=k2, label_visibility="collapsed")
    v3 = c4.number_input(f"{label}_m3", value=v3, key=k3, label_visibility="collapsed")

    return v1, v2, v3

e1, e2, e3 = oh_row("Engine O/H", 700000, 1400000, 0, "e1","e2","e3")
c1v, c2v, c3v = oh_row("Compressor O/H", 500000, 1000000, 0, "c1","c2","c3")

oh1 = e1 + c1v
oh2 = e2 + c2v
oh3 = e3 + c3v

total_row("Major O/H Cost", oh1, oh2, oh3)
st.markdown("---")

# ================= DOWNTIME =================
c1, _, _, _ = st.columns(COLS)
c1.markdown("**Total Downtime**")

inc1, inc2, inc3 = single_row("Income / Hr", 5000, "inc")
lab1, lab2, lab3 = single_row("Idle Labor Cost / Hr", 1000, "lab")
pen1, pen2, pen3 = row("Penalty Cost / Hr", 500, 500, 0, "pen1","pen2","pen3")
d1, d2, d3 = row("Downtime/year", 200, 400, 0, "d1","d2","d3")

down1 = (inc1 + lab1 + pen1) * d1 * y1
down2 = (inc2 + lab2 + pen2) * d2 * y2
down3 = (inc3 + lab3 + pen3) * d3 * y3

total_row("Total Downtime Impact", down1, down2, down3)
st.markdown("---")

# ================= BREAKDOWN =================
c1, _, _, _ = st.columns(COLS)
c1.markdown("**Breakdown Cost**")

b1, b2, b3 = row("Breakdown Repair Cost", 300000, 500000, 0, "b1","b2","b3")
f1, f2, f3 = row("Breakdowns/year", 1, 2, 0, "f1","f2","f3")

break1 = b1 * f1 * y1
break2 = b2 * f2 * y2
break3 = b3 * f3 * y3

total_row("Breakdown Cost", break1, break2, break3)

st.markdown("---")

c1, _, _, _ = st.columns(COLS)
c1.markdown("**Cost of Replacement**")

rep_cost1, rep_cost2, rep_cost3 = row(
    "Replacement Cost",
    200000, 300000, 0,
    "rep_cost1", "rep_cost2", "rep_cost3"
)

rep_freq1, rep_freq2, rep_freq3 = row(
    "Replacements/year",
    1, 2, 0,
    "rep_freq1", "rep_freq2", "rep_freq3"
)

rep1 = rep_cost1 * rep_freq1 * y1
rep2 = rep_cost2 * rep_freq2 * y2
rep3 = rep_cost3 * rep_freq3 * y3

total_row("Total Replacement Cost", rep1, rep2, rep3)
# ================= FINAL =================
op1 = fuel1 + maint1 + oh1 + down1 + break1 + rep1
op2 = fuel2 + maint2 + oh2 + down2 + break2 + rep2
op3 = fuel3 + maint3 + oh3 + down3 + break3 + rep3

tco1 = price1 + op1
tco2 = price2 + op2
tco3 = price3 + op3

fuel_saving = max(0, fuel2 - fuel1)
maint_oh_saving = max(0, (maint2 + oh2) - (maint1 + oh1))
breakdown_saving_actual = max(0, break2 - break1)

def donut_chart_plotly(values, labels, title, total):

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]),
        textinfo='none'   # ❌ remove % text
    )])

    fig.update_layout(
        height=260,
        margin=dict(t=20, b=20, l=0, r=0),
        showlegend=False,   # ❌ remove plotly legend
        annotations=[
            dict(
                text=f"{title}<br><b>{symbol} {total*rate:,.0f}</b>",
                x=0.5, y=0.5,
                font_size=13,
                showarrow=False
            )
        ]
    )

    return fig

st.markdown("---")
calculate = st.button("Calculate TCO")
st.markdown("---")
# ================= RESULT =================
if calculate:
    with result_container:
        st.markdown("### Total Cost of Ownership")

    header()
    total_row("TCO", tco1, tco2, tco3)
    saving_pct_2 = ((tco2 - tco1) / tco2 * 100) if tco2 > 0 else 0
    saving_pct_3 = ((tco3 - tco1) / tco3 * 100) if tco3 > 0 else 0

    # ================= SAVINGS =================

    fuel_saving_2 = max(0, fuel2 - fuel1)
    fuel_saving_3 = max(0, fuel3 - fuel1)

    maint_oh_saving_2 = max(0, (maint2 + oh2) - (maint1 + oh1))
    maint_oh_saving_3 = max(0, (maint3 + oh3) - (maint1 + oh1))

    breakdown_saving_2 = max(0, break2 - break1)
    breakdown_saving_3 = max(0, break3 - break1)

    # % calculation
    fuel_pct_2 = (fuel_saving_2 / fuel2 * 100) if fuel2 > 0 else 0
    fuel_pct_3 = (fuel_saving_3 / fuel3 * 100) if fuel3 > 0 else 0

    maint_oh_pct_2 = (maint_oh_saving_2 / (maint2 + oh2) * 100) if (maint2 + oh2) > 0 else 0
    maint_oh_pct_3 = (maint_oh_saving_3 / (maint3 + oh3) * 100) if (maint3 + oh3) > 0 else 0

    break_pct_2 = (breakdown_saving_2 / break2 * 100) if break2 > 0 else 0
    break_pct_3 = (breakdown_saving_3 / break3 * 100) if break3 > 0 else 0

    rep_saving_2 = max(0, rep2 - rep1)
    rep_saving_3 = max(0, rep3 - rep1)

    rep_pct_2 = (rep_saving_2 / rep2 * 100) if rep2 > 0 else 0
    rep_pct_3 = (rep_saving_3 / rep3 * 100) if rep3 > 0 else 0
    # ================= DISPLAY =================

    st.markdown("#### Extra Cost Compared to Machine 1")
    st.caption("Values show how much more expensive competitors are compared to Machine 1")
    # Header (aligned with main table)
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("**Component**")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown("**Machine 2**")
    c4.markdown("**Machine 3**")

    # -------- Fuel --------
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Fuel Saving")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown(f"{symbol} {fuel_saving_2*rate:,.0f} ({fuel_pct_2:.1f}%)")
    c4.markdown(f"{symbol} {fuel_saving_3*rate:,.0f} ({fuel_pct_3:.1f}%)")

    # -------- Maintenance --------
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Maintenance & O/H")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown(f"{symbol} {maint_oh_saving_2*rate:,.0f} ({maint_oh_pct_2:.1f}%)")
    c4.markdown(f"{symbol} {maint_oh_saving_3*rate:,.0f} ({maint_oh_pct_3:.1f}%)")

    # -------- Breakdown --------
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Breakdown Saving")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown(f"{symbol} {breakdown_saving_2*rate:,.0f} ({break_pct_2:.1f}%)")
    c4.markdown(f"{symbol} {breakdown_saving_3*rate:,.0f} ({break_pct_3:.1f}%)")

    # -------- Replacement --------
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("Replacement Saving")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown(f"{symbol} {rep_saving_2*rate:,.0f} ({rep_pct_2:.1f}%)")
    c4.markdown(f"{symbol} {rep_saving_3*rate:,.0f} ({rep_pct_3:.1f}%)")
    
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown("**Total Saving (%)**")
    c2.markdown("&nbsp;", unsafe_allow_html=True)
    c3.markdown("**Machine 2**")
    c4.markdown("**Machine 3**")

    # Value row
    c1, c2, c3, c4 = st.columns(COLS)

    c1.markdown("Saving (%)")
    c2.markdown("&nbsp;", unsafe_allow_html=True)

    color2 = "green" if saving_pct_2 > 0 else "red"
    color3 = "green" if saving_pct_3 > 0 else "red"

    c3.markdown(
        f"<span style='color:{color2}; font-weight:600'>{saving_pct_2:.1f}%</span>",
        unsafe_allow_html=True
    )

    c4.markdown(
        f"<span style='color:{color3}; font-weight:600'>{saving_pct_3:.1f}%</span>",
        unsafe_allow_html=True
    )
    # ================= CHART =================

    st.markdown("---")
    st.markdown("##### Cost Breakdown Comparison")

    labels = ["Fuel", "Maintenance", "O/H", "Downtime", "Breakdown", "Replacement"]

    values1 = [fuel1, maint1, oh1, down1, break1, rep1]
    values2 = [fuel2, maint2, oh2, down2, break2, rep2]
    values3 = [fuel3, maint3, oh3, down3, break3, rep3]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            donut_chart_plotly(values1, labels, "Machine 1", tco1),
            width="stretch"
        )

    with col2:
        st.plotly_chart(
            donut_chart_plotly(values2, labels, "Machine 2", tco2),
            width="stretch"
        )

    with col3:
        st.plotly_chart(
            donut_chart_plotly(values3, labels, "Machine 3", tco3),
            width="stretch"
        )
    st.markdown(
        """
        <div style='text-align:center; font-size:12px; margin-top:-10px'>
        <span style='color:#4E79A7;'>●</span> Fuel &nbsp;&nbsp;
        <span style='color:#F28E2B;'>●</span> Maintenance &nbsp;&nbsp;
        <span style='color:#E15759;'>●</span> O/H &nbsp;&nbsp;
        <span style='color:#76B7B2;'>●</span> Downtime &nbsp;&nbsp;
        <span style='color:#59A14F;'>●</span> Breakdown &nbsp;&nbsp;
        <span style='color:#EDC948;'>●</span> Replacement
        </div>
        """,
        unsafe_allow_html=True
    )
    # ================= TOTAL SAVING =================
    st.markdown("---")
    st.markdown("##### 💰 Total Savings")

    best_saving = max(tco2 - tco1, tco3 - tco1)
    best_pct = 0
    base = max(tco2, tco3)

    if base > 0:
        best_pct = (best_saving / base) * 100

    st.metric(
        label="Max Saving (vs Competitors)",
        value=f"{symbol} {best_saving*rate:,.0f}",
        delta=f"{best_pct:.1f}%"
    )

    if best_saving > 0:
        st.success(f"Genuine machine gives best savings 💯")
    else:
        st.error("No savings advantage")
    st.markdown("##### 📊 Savings Breakdown Comparison")

    components = ["Fuel", "Maint+O/H", "Breakdown", "Replacement"]

    # Machine 2 savings
    savings_2 = [
        fuel_saving_2,
        maint_oh_saving_2,
        breakdown_saving_2,
        rep_saving_2
    ]
    # Machine 3 savings
    savings_3 = [
        fuel_saving_3,
        maint_oh_saving_3,
        breakdown_saving_3,
        rep_saving_3
    ]
    fig = go.Figure()
    # Machine 2 bars
    fig.add_trace(go.Bar(
        x=components,
        y=savings_2,
        name="Machine 2",
        text=[f"{symbol} {s*rate:,.0f}" for s in savings_2],
        textposition='outside'
    ))

    # Machine 3 bars
    fig.add_trace(go.Bar(
        x=components,
        y=savings_3,
        name="Machine 3",
        text=[f"{symbol} {s*rate:,.0f}" for s in savings_3],
        textposition='outside'
    ))

    fig.update_layout(
        barmode='group',
        height=350,
        title="Savings Breakdown (vs Competitors)",
        xaxis_title="Component",
        yaxis_title="Savings"
    )
    st.plotly_chart(fig, width="stretch")