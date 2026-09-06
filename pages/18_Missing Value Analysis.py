import pandas as pd
import plotly.express as px
import streamlit as st
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.title("18. Missing Values Analysis")

# 1. Load & Filter Data
df = load_data()
df_filtered = apply_sidebar_filters(df)

# ---------------------------------------------------------
# CALCULATE MISSING DATA STATS
# ---------------------------------------------------------
total_rows, total_cols = df_filtered.shape
total_missing_values = df_filtered.isnull().sum().sum()

# DataFrame summary for columns with missing data
null_counts = df_filtered.isnull().sum()
null_percents = (df_filtered.isnull().mean() * 100).round(2)
dtypes = df_filtered.dtypes.astype(str)

missing_df = pd.DataFrame(
    {
        "Column": df_filtered.columns,
        "Missing Count": null_counts,
        "Missing %": null_percents,
        "Data Type": dtypes,
    }
)
# Keep only columns that have at least 1 missing value
missing_df = (
    missing_df[missing_df["Missing Count"] > 0]
    .sort_values(by="Missing Count", ascending=False)
    .reset_index(drop=True)
)

cols_with_missing = len(missing_df)
cols_gt_50_pct = len(missing_df[missing_df["Missing %"] > 50])

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Rows", f"{total_rows:,}")
c2.metric("Total Columns", f"{total_cols:,}")
c3.metric("Total Missing Values", f"{total_missing_values:,}")
c4.metric("Cols w/ Missing Values", f"{cols_with_missing}")
c5.metric("Cols > 50% Missing", f"{cols_gt_50_pct}")

st.divider()

# ---------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------
st.subheader("Visualizations")
col1, col2 = st.columns(2)

# 1. Top 20 Columns with Missing Values
with col1:
    top_20 = missing_df.head(20)
    fig1 = px.bar(top_20,x="Missing Count",y="Column",orientation="h",
        title="Top 20 Columns with Missing Values",text_auto=",",)
    fig1.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig1, width="stretch")

# 2. Missing Percentage by Column
with col2:
    fig2 = px.bar(top_20,x="Missing %",y="Column",orientation="h",
        title="Missing Percentage by Column (Top 20)",
        text_auto=".1f",)
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, width="stretch")

st.divider()

col3, col4 = st.columns(2)

# 3. Missing Values Heatmap (Sampled for smooth performance)
with col3:
    sample_size = min(500, len(df_filtered))
    sample_top_cols = (
        missing_df.head(15)["Column"].tolist()
        if not missing_df.empty
        else df_filtered.columns[:10]
    )
    heatmap_data = df_filtered[sample_top_cols].head(sample_size).isnull().astype(int)

    fig3 = px.imshow( heatmap_data,labels=dict(x="Columns", y="Sample Rows", color="Is Missing"),
        title=f"Missing Values Heatmap (Top 15 Cols, {sample_size} Rows)",
        color_continuous_scale=["#2ca02c", "#d62728"],  # Green=Present, Red=Missing
    )
    st.plotly_chart(fig3, width="stretch")

# 4. Missing Values by Data Type
with col4:
    missing_by_dtype = (
        missing_df.groupby("Data Type")["Missing Count"].sum().reset_index()
    )
    fig4 = px.pie( missing_by_dtype, names="Data Type", values="Missing Count",
        title="Missing Values by Data Type",
        hole=0.4,
    )
    st.plotly_chart(fig4, width="stretch")

st.divider()

# ---------------------------------------------------------
# TABLE
# ---------------------------------------------------------
st.subheader("Missing Data Details Table")
st.dataframe(missing_df, use_container_width=True)