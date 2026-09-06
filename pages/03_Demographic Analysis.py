import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.set_page_config(page_title="Page 3 – Demographic Analysis", layout="wide")
st.title("Page 3 – Customer Demographic Analysis")
st.write("**Purpose:** Understand demographic characteristics of Home Credit applicants.")

df = load_data()

if df is not None:
    # Preprocess Age & Age Groups
    df['AGE'] = (df['DAYS_BIRTH'].abs() / 365.25).astype(int)
    bins = [0, 25, 35, 50, 65, 100]
    labels = ['<25', '25-34', '35-49', '50-64', '65+']
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=False)
    df_filtered=apply_sidebar_filters(df)

    # Sidebar Filters
    st.sidebar.header("Filters")
    f_gen = st.sidebar.selectbox("Gender", ['All'] + list(df_filtered['CODE_GENDER'].dropna().unique()),key="demo_gender_select",)
    f_age = st.sidebar.selectbox("Age Group", ['All'] + list(df_filtered['AGE_GROUP'].dropna().unique().astype(str)),key="demo_age_select",)
    f_fam = st.sidebar.selectbox("Family Status", ['All'] + list(df_filtered['NAME_FAMILY_STATUS'].dropna().unique()),key="demo_family_select",)
    f_edu = st.sidebar.selectbox("Education", ['All'] + list(df_filtered['NAME_EDUCATION_TYPE'].dropna().unique()),key="demo_edu_select",)
    f_hou = st.sidebar.selectbox("Housing Type", ['All'] + list(df_filtered['NAME_HOUSING_TYPE'].dropna().unique()),key="demo_hou_select",)

    # Apply Filters
    d = df_filtered.copy()
    if f_gen != 'All': d = d[d['CODE_GENDER'] == f_gen]
    if f_age != 'All': d = d[d['AGE_GROUP'] == f_age]
    if f_fam != 'All': d = d[d['NAME_FAMILY_STATUS'] == f_fam]
    if f_edu != 'All': d = d[d['NAME_EDUCATION_TYPE'] == f_edu]
    if f_hou != 'All': d = d[d['NAME_HOUSING_TYPE'] == f_hou]

    # KPI Cards
    st.subheader("KPI Cards")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Customers", f"{len(d):,}")
    c2.metric("Average Age", f"{d['AGE'].mean():.1f} yrs")
    c3.metric("Male Customers", f"{(d['CODE_GENDER'] == 'M').sum():,}")
    c4.metric("Female Customers", f"{(d['CODE_GENDER'] == 'F').sum():,}")
    c5.metric("Avg Family Size", f"{d['CNT_FAM_MEMBERS'].mean():.1f}")

    # Visualizations
    st.divider()
    st.subheader("Visualizations")
    col1, col2 = st.columns(2)

    # Helper function for safe bar charting
    def plot_bar(dataframe, col_name, title, target_col):
        counts = dataframe[col_name].value_counts().reset_index()
        counts.columns = [col_name, 'Count']
        target_col.plotly_chart(px.bar(counts, x=col_name, y='Count', title=title, text_auto=True), use_container_width=True)

    plot_bar(d, 'CODE_GENDER', "Customers by Gender", col1)
    plot_bar(d, 'AGE_GROUP', "Customers by Age Group", col2)
    plot_bar(d, 'NAME_FAMILY_STATUS', "Customers by Family Status", col1)
    plot_bar(d, 'NAME_EDUCATION_TYPE', "Customers by Education", col2)
    plot_bar(d, 'NAME_HOUSING_TYPE', "Customers by Housing Type", col1)

    # Default Rate by Demographic Group (Age)
    def_df = d.groupby('AGE_GROUP', observed=False)['TARGET'].mean().reset_index()
    def_df['Default Rate %'] = def_df['TARGET'] * 100
    col2.plotly_chart(px.line(def_df, x='AGE_GROUP', y='Default Rate %', title="Default Rate by Age Group", markers=True), use_container_width=True)