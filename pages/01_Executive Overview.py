import sys
from pathlib import Path


import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.kpis import get_kpis

# Page configuration
st.set_page_config(page_title="Executive Overview", layout="wide")

st.title("📊 Executive Overview")
st.markdown("---")

# 1. Load Data & Compute KPIs
df = load_data("merge_data.csv", nrows=1000)
kpis = get_kpis(df)

# 2. First Row of KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Application", f"{kpis['Total Application']}")
col2.metric("Total Default Customer", f"{kpis['Total default customer']}")
col3.metric("Total Non-Default Customer", f"{kpis['Total non default customer']}")
col4.metric("Default Rate %", f"{kpis['Default rate']}")

st.markdown("---")

# 3. Second Row of KPI Metrics
col5, col6, col7, col8 = st.columns(4)
col5.metric("Avg Credit Amount", f"{kpis['avg credit amount']}")
col6.metric("Avg Income", f"{kpis['Avg Income']}")
col7.metric("Avg Annuity", f"{kpis['Avg annuity']}")
col8.metric("Total Credit Exposure", f"{kpis['Total credit']}")

st.markdown("---")

# 4. Target Distribution Bar Chart
default_counts = df["TARGET"].value_counts().reset_index()
default_counts.columns = ["TARGET", "Count"]

fig = px.bar(
    default_counts,
    x="TARGET",
    y="Count",
    color="TARGET",
    title="Target Distribution",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
