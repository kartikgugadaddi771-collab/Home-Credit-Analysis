import streamlit as st, plotly.express as px, pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="Page 4 – Age Analysis", layout="wide")
st.title("Page 4 – Age Analysis")
st.write("**Purpose:** Analyze the relationship between age and credit risk.")

df = load_data()
if df is not None and 'DAYS_BIRTH' in df.columns:
    df['AGE'] = (df['DAYS_BIRTH'].abs() / 365).astype(int)
    bins, labels = [18, 25, 30, 35, 40, 45, 50, 55, 60, 100], ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61+']
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=True)

    # KPI Cards
    st.subheader("KPI Cards")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Age", f"{df['AGE'].mean():.1f} yrs")
    c2.metric("Youngest Customer", f"{df['AGE'].min()} yrs")
    c3.metric("Oldest Customer", f"{df['AGE'].max()} yrs")
    risk_grp = df.groupby('AGE_GROUP', observed=False)['TARGET'].mean().idxmax() if 'TARGET' in df.columns else "N/A"
    c4.metric("Highest Risk Age Group", f"{risk_grp}")

    # Visualizations
    st.divider()
    st.subheader("Visualizations")
    col1, col2 = st.columns(2)

    col1.plotly_chart(px.histogram(df, x='AGE', nbins=30, title="Age Distribution Histogram"), use_container_width=True)
    
    app_cnt = df['AGE_GROUP'].value_counts().reset_index().rename(columns={'index':'AGE_GROUP', 'count':'Applications'})
    col2.plotly_chart(px.bar(app_cnt, x='AGE_GROUP', y='Applications', title="Applications by Age Group", text_auto=True), use_container_width=True)

    if 'TARGET' in df.columns:
        col1.plotly_chart(px.line(df.groupby('AGE')['TARGET'].mean().reset_index().assign(Rate=lambda x: x['TARGET']*100), x='AGE', y='Rate', title="Default Rate by Age"), use_container_width=True)
        def_grp = df.groupby('AGE_GROUP', observed=False)['TARGET'].mean().reset_index().assign(Rate=lambda x: x['TARGET']*100)
        col2.plotly_chart(px.bar(def_grp, x='AGE_GROUP', y='Rate', title="Default Rate by Age Group", text_auto='.2f'), use_container_width=True)

    if 'AMT_CREDIT' in df.columns:
        col1.plotly_chart(px.line(df.groupby('AGE')['AMT_CREDIT'].mean().reset_index(), x='AGE', y='AMT_CREDIT', title="Credit Amount by Age"), use_container_width=True)
    if 'AMT_INCOME_TOTAL' in df.columns:
        col2.plotly_chart(px.line(df.groupby('AGE')['AMT_INCOME_TOTAL'].mean().reset_index(), x='AGE', y='AMT_INCOME_TOTAL', title="Income by Age"), use_container_width=True)