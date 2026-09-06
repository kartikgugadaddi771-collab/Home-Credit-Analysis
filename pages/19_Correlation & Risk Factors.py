import pandas as pd
import plotly.express as px
import streamlit as st
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.title("19. Correlation & Risk Factors Analysis")

# 1. Load Data & Filter
df = load_data()
df_filtered = apply_sidebar_filters(df)

# Selected Numerical Features
cols = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
]
num_df = df_filtered[[c for c in cols if c in df_filtered.columns]].dropna()

# Calculate Correlations
corr = num_df.corr()
target_corr = corr["TARGET"].drop("TARGET").sort_values()

# ---------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------
st.subheader("Correlation Analysis")
c1, c2 = st.columns(2)

# 1. Heatmap
with c1:
    fig1 = px.imshow(
        corr, text_auto=".2f", title="Correlation Heatmap", aspect="auto"
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2. Correlation with TARGET
with c2:
    fig2 = px.bar(
        x=target_corr.values,y=target_corr.index,
        orientation="h",title="Correlation with TARGET",)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4= st.columns(2)

# 3. Top Positive & Negative Correlations
with c3:
    
    top_pos_neg = pd.concat([target_corr.tail(3), target_corr.head(3)])
    fig3 = px.bar(x=top_pos_neg.values,y=top_pos_neg.index,orientation="h",
        title="Top Positive & Negative Correlations with Target",color=top_pos_neg.values > 0,
        color_discrete_map={True: "red", False: "green"},)
    st.plotly_chart(fig3, use_container_width=True)

# 4. Scatter: Credit vs Income

    fig4 = px.scatter( df_filtered.head(1000),x="AMT_INCOME_TOTAL",y="AMT_CREDIT",
        color="TARGET",title="Credit vs Income Scatter",)
    st.plotly_chart(fig4, use_container_width=True)

# 5. External Score vs TARGET
df_filtered["AVG_EXT_SOURCE"] = df_filtered[
    ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
].mean(axis=1)
fig5 = px.box(df_filtered,x="TARGET",y="AVG_EXT_SOURCE",
    title="External Score vs TARGET (0 = Repaid, 1 = Default)",)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# IMPORTANT RISK FACTORS SECTION
# ---------------------------------------------------------
st.subheader("Important Risk Indicators")
st.markdown(
    """
* **Low External Credit Score:** Lower average external scores strongly correlate with higher default rates.
* **High Credit-to-Income Ratio:** Borrowers taking credit far exceeding their total income present higher risk.
* **High Annuity-to-Income Ratio:** High monthly payments relative to income strain repayment capacity.
* **Certain Occupations & Income Types:** Specific job types (e.g., Low-skill Laborers) show higher default trends.
* **Younger Age Groups:** Younger applicants (`DAYS_BIRTH` closer to 0) historically have higher default rates.
* **Regional Risk Rating & Employment History:** High regional risk ratings and shorter employment tenure increase default likelihood.
"""
)