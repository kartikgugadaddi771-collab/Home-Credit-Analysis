import plotly.express as px
import streamlit as st
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.title("17. Regional Risk Analysis")

# 1. Load & Filter Data
df = load_data()
df_filtered=apply_sidebar_filters(df)
most_common_rating = df_filtered["REGION_RATING_CLIENT"].mode()[0]

# Highest Risk Region Rating (Rating with max default rate)
rating_def_rates = (df_filtered.groupby("REGION_RATING_CLIENT")["TARGET"].mean().mul(100))
highest_risk_rating = rating_def_rates.idxmax()

# Average Regional Population Indicator
avg_pop = df_filtered["REGION_POPULATION_RELATIVE"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Most Common Region Rating", f"Rating {most_common_rating}")
c2.metric("Highest Risk Region Rating", f"Rating {highest_risk_rating}")
c3.metric("Avg Regional Population", f"{avg_pop:.4f}")

st.divider()

col1, col2 = st.columns(2)

# Visual 1: Customers by Region Rating
with col1:
    cust_by_rating = (df_filtered["REGION_RATING_CLIENT"].value_counts() .reset_index(name="Customer Count") )
    fig1 = px.bar(cust_by_rating,x="REGION_RATING_CLIENT",y="Customer Count",title="Customers by Region Rating",text_auto=",",)
    st.plotly_chart(fig1, width="stretch")

# Visual 2: Default Rate by Region Rating
with col2:
    def_by_rating = rating_def_rates.reset_index(name="Default Rate (%)")
    fig2 = px.bar(def_by_rating,
        x="REGION_RATING_CLIENT",y="Default Rate (%)",title="Default Rate by Region Rating",
        text_auto=".2f", )
    st.plotly_chart(fig2, width="stretch")

st.divider()

# ---------------------------------------------------------
# VISUALIZATIONS (Row 2)
# ---------------------------------------------------------
col3, col4 = st.columns(2)

# Visual 3: Credit by Region Rating
with col3:
    fig3 = px.box(df_filtered,x="REGION_RATING_CLIENT",y="AMT_CREDIT",
        title="Credit Amount by Region Rating", )
    st.plotly_chart(fig3, width="stretch")

# Visual 4: Income by Region Rating
with col4:
    fig4 = px.box(df_filtered,x="REGION_RATING_CLIENT",y="AMT_INCOME_TOTAL",title="Income by Region Rating", )
    st.plotly_chart(fig4, width="stretch")
st.divider()

# ---------------------------------------------------------
# VISUALIZATIONS (Row 3 - Mismatch Analysis)
# ---------------------------------------------------------
col5, col6 = st.columns(2)

# Visual 5: Region Mismatch vs Default (Live vs Work Region)
with col5:
    region_mismatch = (df_filtered.groupby("REG_REGION_NOT_WORK_REGION")["TARGET"].mean().mul(100)
        .reset_index())
    region_mismatch["REG_REGION_NOT_WORK_REGION"] = region_mismatch[
        "REG_REGION_NOT_WORK_REGION"].map({0: "Same Region", 1: "Region Mismatch"})
    fig5 = px.bar(region_mismatch,x="REG_REGION_NOT_WORK_REGION",y="TARGET",
        title="Region Mismatch vs Default Rate (%)",
        text_auto=".2f",)
    st.plotly_chart(fig5, width="stretch")

# Visual 6: City Mismatch vs Default (Live vs Work City)
with col6:
    city_mismatch = (
        df_filtered.groupby("REG_CITY_NOT_WORK_CITY")["TARGET"]
        .mean()
        .mul(100)
        .reset_index()
    )
    city_mismatch["REG_CITY_NOT_WORK_CITY"] = city_mismatch[
        "REG_CITY_NOT_WORK_CITY"
    ].map({0: "Same City", 1: "City Mismatch"})
    fig6 = px.bar( city_mismatch, x="REG_CITY_NOT_WORK_CITY",y="TARGET",
                  title="City Mismatch vs Default Rate (%)", text_auto=".2f",)
    st.plotly_chart(fig6, width="stretch")