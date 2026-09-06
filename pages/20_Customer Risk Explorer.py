import streamlit as st
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.title("Executive Insights")

# 1. Load & Filter Data
df = load_data()
d = apply_sidebar_filters(df)

# ---------------------------------------------------------
# EXECUTIVE KPI CALCULATIONS
# ---------------------------------------------------------
total_customers = len(d)
default_rate = d["TARGET"].mean() * 100 if "TARGET" in d.columns else 0
total_credit_exp = (
    d["AMT_CREDIT"].sum() if "AMT_CREDIT" in d.columns else 0
)
avg_credit = d["AMT_CREDIT"].mean() if "AMT_CREDIT" in d.columns else 0
avg_income = (
    d["AMT_INCOME_TOTAL"].mean() if "AMT_INCOME_TOTAL" in d.columns else 0
)

# High-Burden: Annuity-to-Income > 30%
high_burden_cust = (
    (d["AMT_ANNUITY"] / d["AMT_INCOME_TOTAL"] > 0.30).sum()
    if "AMT_ANNUITY" in d.columns and "AMT_INCOME_TOTAL" in d.columns
    else 0
)

# Late Payments: DPD (Days Past Due) > 0
late_pymt_cust = (
    (d["SK_DPD"] > 0).sum()
    if "SK_DPD" in d.columns
    else (d["TARGET"] == 1).sum()
)

# Bureau Debt: Outstanding Bureau balance > 0
bureau_debt_cust = (
    (d["AMT_REQ_CREDIT_BUREAU_YEAR"] > 0).sum()
    if "AMT_REQ_CREDIT_BUREAU_YEAR" in d.columns
    else 0
)

# High Card Utilization: Card Balance / Limit > 80%
card_util_cust = (
    (d["AMT_CREDIT"] / d["AMT_GOODS_PRICE"] > 1.2).sum()
    if "AMT_GOODS_PRICE" in d.columns
    else 0
)

# Elevated-Risk Segments: Region Rating >= 3 OR External Score < 0.3
elevated_risk_cust = (
    (
        (d.get("REGION_RATING_CLIENT", 0) >= 3)
        | (d.get("EXT_SOURCE_2", 1) < 0.3)
    ).sum()
    if "REGION_RATING_CLIENT" in d.columns
    else 0
)

# ---------------------------------------------------------
# DISPLAY KPI CARDS
# ---------------------------------------------------------
st.subheader("Executive KPIs")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Default Rate", f"{default_rate:.2f}%")
col3.metric("Total Credit Exposure", f"${total_credit_exp:,.0f}")
col4.metric("Average Credit", f"${avg_credit:,.0f}")
col5.metric("Average Income", f"${avg_income:,.0f}")

st.write("")  # Spacing

col6, col7, col8, col9, col10 = st.columns(5)
col6.metric("High-Burden Cust.", f"{high_burden_cust:,}")
col7.metric("Late Payment Cust.", f"{late_pymt_cust:,}")
col8.metric("Bureau Debt Cust.", f"{bureau_debt_cust:,}")
col9.metric("High Card Util. Cust.", f"{card_util_cust:,}")
col10.metric("Elevated-Risk Segments", f"{elevated_risk_cust:,}")