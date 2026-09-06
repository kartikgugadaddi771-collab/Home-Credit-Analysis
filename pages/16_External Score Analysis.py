import plotly.express as px
import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.title("External Sources Risk Analysis")

# 1. Load & Filter Data
df = load_data()
df_filtered = apply_sidebar_filters(df)

# 2. Derived Feature: Average External Score
df_filtered["AVG_EXT_SOURCE"] = df_filtered[
    ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
].mean(axis=1)


c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg EXT_SOURCE_1", f"{df_filtered['EXT_SOURCE_1'].mean():.2f}")
c2.metric("Avg EXT_SOURCE_2", f"{df_filtered['EXT_SOURCE_2'].mean():.2f}")
c3.metric("Avg EXT_SOURCE_3", f"{df_filtered['EXT_SOURCE_3'].mean():.2f}")
c4.metric("Overall Avg Score", f"{df_filtered['AVG_EXT_SOURCE'].mean():.2f}")

st.divider()


col1, col2, col3 = st.columns(3)

with col1:
    fig1 = px.histogram(
        df_filtered, x="EXT_SOURCE_1", title="EXT_SOURCE_1 Distribution"
    )
    st.plotly_chart(fig1, width="stretch")

with col2:
    fig2 = px.histogram(
        df_filtered, x="EXT_SOURCE_2", title="EXT_SOURCE_2 Distribution"
    )
    st.plotly_chart(fig2, width="stretch")

with col3:
    fig3 = px.histogram(
        df_filtered, x="EXT_SOURCE_3", title="EXT_SOURCE_3 Distribution"
    )
    st.plotly_chart(fig3, width="stretch")

st.divider()

# ---------------------------------------------------------
# VISUALIZATIONS: Target & Default Rate Comparisons
# ---------------------------------------------------------
col4, col5 = st.columns(2)

# Scores by TARGET (Boxplot)
with col4:
    fig4 = px.box(df_filtered,x="TARGET",y="AVG_EXT_SOURCE",
        title="Average Score by Target (0 = Repaid, 1 = Default)",)
    st.plotly_chart(fig4, width="stretch")

# External Score vs Default Rate
with col5:
    # Group scores into Low, Medium, High
    df_filtered["SCORE_GROUP"] = pd.cut(df_filtered["AVG_EXT_SOURCE"], bins=[0, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"],
    )
    risk_df = (df_filtered.groupby("SCORE_GROUP", observed=False)["TARGET"].mean().mul(100)
        .reset_index())

    fig5 = px.bar(risk_df,x="SCORE_GROUP",y="TARGET",title="Default Rate (%) by Score Level",
        text_auto=".2f",)
    st.plotly_chart(fig5, width="stretch")

st.divider()

# ---------------------------------------------------------
# VISUALIZATIONS: Scatter Comparisons
# ---------------------------------------------------------
col6, col7 = st.columns(2)

with col6:
    fig6 = px.scatter(df_filtered.head(1000),x="EXT_SOURCE_1",y="EXT_SOURCE_2",color="TARGET",
        title="EXT_1 vs EXT_2",
    )
    st.plotly_chart(fig6, width="stretch")

with col7:
    fig7 = px.scatter(df_filtered.head(1000),x="EXT_SOURCE_2",y="EXT_SOURCE_3",color="TARGET",
        title="EXT_2 vs EXT_3",
    )
    st.plotly_chart(fig7, width="stretch")