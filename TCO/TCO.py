import streamlit as st
import pandas as pd

st.set_page_config(page_title="TCO Tool", layout="wide")

# ================= LOAD =================
@st.cache_data
def load_data():
    df = pd.read_excel("CPPT.xlsx", sheet_name=0)
    df = df[df["Description"].notna()]
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 🔥 DISPLAY COPY (for UI)
df_display = df.copy()

# 🔥 CLEAN FOR MATCHING (backend)
df["Competitor(Machine 2)"] = df["Competitor(Machine 2)"].astype(str).str.strip().str.lower()
df["Machine 3"] = df["Machine 3"].astype(str).str.strip().str.lower()
df["Description"] = df["Description"].astype(str).str.strip()

df_display["Competitor(Machine 2)"] = df_display["Competitor(Machine 2)"].astype(str).str.strip()
df_display["Machine 3"] = df_display["Machine 3"].astype(str).str.strip()

# ================= RESULT =================
result_container = st.container()
COLS = [2,1,1,1]

# ================= MACHINE =================
c0, c1, c2, c3 = st.columns(COLS)

with c0:
    st.markdown("Machine Selection")

with c1:
    machine1 = st.selectbox("Machine 1", df_display["Description"])

    row1 = df[df["Description"] == machine1]
    price_val = row1["CLP 2026"].values[0] if not row1.empty else 0
    new_price1 = 0 if pd.isna(price_val) else int(price_val)

    if "price1_input" not in st.session_state or st.session_state.price1_input != new_price1:
        st.session_state.price1_input = new_price1

with c2:
    machine2_list = df_display["Competitor(Machine 2)"].dropna().unique().tolist()
    machine2 = st.selectbox("Machine 2", machine2_list, index=0)

with c3:
    machine3_list = df_display["Machine 3"].dropna().unique().tolist()
    machine3 = st.selectbox("Machine 3", machine3_list, index=0)

st.markdown("---")

# 🔥 CLEAN INPUT FOR MATCHING
machine2_clean = str(machine2).strip().lower()
machine3_clean = str(machine3).strip().lower()

# ================= PRICE =================
row2 = df[df["Competitor(Machine 2)"] == machine2_clean]
price2_val = int(row2["Machine 2 Price"].values[0]) if not row2.empty else 0

row3 = df[df["Machine 3"] == machine3_clean]
price3_val = int(row3["Machine 3 Price"].values[0]) if not row3.empty else 0

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
    v1 = c2.number_input(" ", value=v1, key=k1, min_value=0, label_visibility="collapsed")
    v2 = c3.number_input(" ", value=v2, key=k2, min_value=0, label_visibility="collapsed")
    v3 = c4.number_input(" ", value=v3, key=k3, min_value=0, label_visibility="collapsed")
    return v1, v2, v3

def total_row(label, v1, v2, v3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(f"**{label}**")
    c2.markdown(f"₹ {v1:,.0f}")
    c3.markdown(f"₹ {v2:,.0f}")
    c4.markdown(f"₹ {v3:,.0f}")

header()

# ================= INITIAL COST =================
c1, c2, c3, c4 = st.columns(COLS)
c1.markdown("Initial Cost")

price1 = c2.number_input(" ", key="price1_input", disabled=True, min_value=0, label_visibility="collapsed")

# Machine 2
if "price2_input" not in st.session_state:
    st.session_state.price2_input = price2_val

if "last_machine2" not in st.session_state:
    st.session_state.last_machine2 = machine2_clean

if machine2_clean != st.session_state.last_machine2:
    st.session_state.price2_input = price2_val
    st.session_state.last_machine2 = machine2_clean

price2 = c3.number_input(" ", key="price2_input", min_value=0, label_visibility="collapsed")

# Machine 3
if "price3_input" not in st.session_state:
    st.session_state.price3_input = price3_val

if "last_machine3" not in st.session_state:
    st.session_state.last_machine3 = machine3_clean

if machine3_clean != st.session_state.last_machine3:
    st.session_state.price3_input = price3_val
    st.session_state.last_machine3 = machine3_clean

price3 = c4.number_input(" ", key="price3_input", min_value=0, label_visibility="collapsed")

st.markdown("---")

# ================= FUEL =================
fp1, fp2, fp3 = row("Fuel Cost/L", 93, 93, 0, "fp1","fp2","fp3")
fc1, fc2, fc3 = row("Fuel Consumption/Hr", 65, 70, 0, "fc1","fc2","fc3")
h1, h2, h3 = row("Running Hours/year", 2000, 2000, 0, "h1","h2","h3")
y1, y2, y3 = row("Total Years", 10, 10, 0, "y1","y2","y3")

fuel1 = fp1 * fc1 * h1 * y1
fuel2 = fp2 * fc2 * h2 * y2
fuel3 = fp3 * fc3 * h3 * y3

total_row("Fuel Cost (Total)", fuel1, fuel2, fuel3)
st.markdown("---")

# ================= MAINTENANCE =================
c1, c2, c3, c4 = st.columns(COLS)
c1.markdown("Maintenance / Year")

m1 = c2.number_input(" ", value=218000, key="m1", min_value=0, label_visibility="collapsed")
m2 = c3.number_input(" ", value=109000, key="m2", min_value=0, label_visibility="collapsed")
m3 = c4.number_input(" ", value=0, key="m3", min_value=0, label_visibility="collapsed")

maint1 = m1 * y1
maint2 = m2 * y2
maint3 = m3 * y3

total_row("Maintenance Cost (Total)", maint1, maint2, maint3)
st.markdown("---")

# ================= O/H =================
parts = st.radio("Machine 1 Parts Type", ["Genuine", "Non-Genuine"])

disable_m1_oh = parts == "Genuine" and ((y1 < 5) or (h1 < 1500))

def oh_row(label, v1, v2, v3, k1, k2, k3):
    c1, c2, c3, c4 = st.columns(COLS)
    c1.markdown(label)
    v1 = c2.number_input(" ", value=v1, key=k1, disabled=disable_m1_oh, min_value=0, label_visibility="collapsed")
    v2 = c3.number_input(" ", value=v2, key=k2, min_value=0, label_visibility="collapsed")
    v3 = c4.number_input(" ", value=v3, key=k3, min_value=0, label_visibility="collapsed")
    return v1, v2, v3

e1, e2, e3 = oh_row("Engine O/H", 700000, 1400000, 0, "e1","e2","e3")
c1v, c2v, c3v = oh_row("Compressor O/H", 500000, 1000000, 0, "c1","c2","c3")

if disable_m1_oh:
    e1, c1v = 0, 0

oh1 = e1 + c1v
oh2 = e2 + c2v
oh3 = e3 + c3v

total_row("Major O/H Cost", oh1, oh2, oh3)
st.markdown("---")

# ================= DOWNTIME =================
inc1, inc2, inc3 = row("Per Hour Income", 5000, 5000, 0, "inc1","inc2","inc3")
d1, d2, d3 = row("Downtime/year", 200, 400, 0, "d1","d2","d3")

down1 = inc1 * d1 * y1
down2 = inc2 * d2 * y2
down3 = inc3 * d3 * y3

total_row("Downtime Cost", down1, down2, down3)
st.markdown("---")

# ================= FINAL =================
op1 = fuel1 + maint1 + oh1 + down1
op2 = fuel2 + maint2 + oh2 + down2
op3 = fuel3 + maint3 + oh3 + down3

tco1 = price1 + op1
tco2 = price2 + op2
tco3 = price3 + op3

fuel_saving = fuel2 - fuel1
breakdown_saving = max(0, (maint2 + oh2) - (maint1 + oh1))

# ================= RESULT =================
with result_container:
    st.markdown("### Total Cost of Ownership")

    header()
    total_row("TCO", tco1, tco2, tco3)

    c1, c2, _, _ = st.columns(COLS)
    c1.markdown("Fuel Saving")
    c2.markdown(f"₹ {fuel_saving:,.0f}")

    c1, c2, _, _ = st.columns(COLS)
    c1.markdown("Breakdown Saving")
    c2.markdown(f"₹ {breakdown_saving:,.0f}")