import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.filters import apply_sidebar_filters

st.set_page_config(page_title="Page 2 – Target / Default Analysis", page_icon="🎯", layout="wide")

# Title & Purpose
st.title("Page 2 – Target / Default Analysis")
st.subheader("Purpose")
st.write("Analyze the main TARGET variable.")

df = load_data()
df_filtered=apply_sidebar_filters(df)

if df is not None and 'TARGET' in df.columns:
    # Key Calculations
    total_customers = len(df)
    target_0_count = (df_filtered['TARGET'] == 0).sum()
    target_1_count = (df_filtered['TARGET'] == 1).sum()
    
    default_rate = (target_1_count / total_customers) * 100 if total_customers > 0 else 0
    non_default_rate = (target_0_count / total_customers) * 100 if total_customers > 0 else 0

    # KPI Cards
    st.subheader("KPI Cards")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TARGET = 0 Customers", f"{target_0_count:,}")
    col2.metric("TARGET = 1 Customers", f"{target_1_count:,}")
    col3.metric("Default Rate %", f"{default_rate:.2f}%")
    col4.metric("Non-Default Rate %", f"{non_default_rate:.2f}%")

    st.divider()
    st.subheader("Visualizations")

    # Row 1: Target Count & Donut Chart
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        # TARGET Count Bar Chart
        target_counts = df_filtered['TARGET'].value_counts().reset_index()
        target_counts.columns = ['TARGET', 'Count']
        target_counts['TARGET'] = target_counts['TARGET'].astype(str)
        
        fig_bar = px.bar(
            target_counts, x='TARGET', y='Count', 
            title="TARGET Count Bar Chart", text_auto=True,
            color='TARGET', color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with row1_col2:
        # TARGET Percentage Pie/Donut Chart
        fig_donut = px.pie(
            target_counts, names='TARGET', values='Count', hole=0.4,
            title="TARGET Percentage Pie/Donut Chart",
            color='TARGET', color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig_donut.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_donut, use_container_width=True)

    # Row 2: Default Rate Breakdown Visualizations
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        if 'CODE_GENDER' in df.columns:
            gender_df = df_filtered.groupby('CODE_GENDER')['TARGET'].mean().reset_index()
            gender_df['Default Rate %'] = gender_df['TARGET'] * 100
            fig_gender = px.bar(gender_df, x='CODE_GENDER', y='Default Rate %', title="Default Rate by Gender", text_auto='.2f')
            st.plotly_chart(fig_gender, use_container_width=True)

    with row2_col2:
        if 'NAME_INCOME_TYPE' in df.columns:
            income_df = df_filtered.groupby('NAME_INCOME_TYPE')['TARGET'].mean().reset_index()
            income_df['Default Rate %'] = income_df['TARGET'] * 100
            fig_income = px.bar(income_df, x='NAME_INCOME_TYPE', y='Default Rate %', title="Default Rate by Income Type", text_auto='.2f')
            st.plotly_chart(fig_income, use_container_width=True)

    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        if 'NAME_EDUCATION_TYPE' in df.columns:
            edu_df = df_filtered.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean().reset_index()
            edu_df['Default Rate %'] = edu_df['TARGET'] * 100
            fig_edu = px.bar(edu_df, x='NAME_EDUCATION_TYPE', y='Default Rate %', title="Default Rate by Education", text_auto='.2f')
            st.plotly_chart(fig_edu, use_container_width=True)

    with row3_col2:
        if 'NAME_CONTRACT_TYPE' in df.columns:
            contract_df = df_filtered.groupby('NAME_CONTRACT_TYPE')['TARGET'].mean().reset_index()
            contract_df['Default Rate %'] = contract_df['TARGET'] * 100
            fig_contract = px.bar(contract_df, x='NAME_CONTRACT_TYPE', y='Default Rate %', title="Default Rate by Contract Type", text_auto='.2f')
            st.plotly_chart(fig_contract, use_container_width=True)

else:
    st.error("Missing required column 'TARGET' in dataset.")