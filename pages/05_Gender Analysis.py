import streamlit as st
import pandas as pd
import os
import sys

from utils.data_loader import load_data
from utils.charts import plot_bar_by_category,histogram_chart

st.title("5. GENDER ANALYSIS")

df=load_data()

c1,c2,c3,c4 =st.columns(4)
male_count = (df["CODE_GENDER"] == "M").sum()
c1.metric("Male applicants", male_count)
female_count = (df["CODE_GENDER"] == "F").sum()
c2.metric("Female applicants", female_count)
male_default_rate = df.loc[df["CODE_GENDER"] =="M","TARGET"].mean()*100
c3.metric("Male Default Rate",f"{male_default_rate:.2f}" )
female_default_rate = df.loc[df["CODE_GENDER"] == "F", "TARGET"].mean() * 100
c4.metric("Female Default Rate", f"{female_default_rate:.2f}")

st.subheader("1. Total Application By Gender")
st.plotly_chart(plot_bar_by_category(df,"CODE_GENDER","Application Count By Gender"))

st.subheader("2. Default Rate By Gender")
st.plotly_chart(plot_bar_by_category(df,"CODE_GENDER","Default Rate by Gender"))

st.subheader("Avg_Income By Gender")
avg_income=df.groupby("CODE_GENDER")["AMT_INCOME_TOTAL"].mean().reset_index()
st.bar_chart(avg_income.set_index("CODE_GENDER"))

st.subheader("Average Loan Amount By Gender")
avg_loan_amount=df.groupby("CODE_GENDER")["AMT_CREDIT"].mean().reset_index()
st.bar_chart(avg_loan_amount.set_index("CODE_GENDER"))

st.markdown("**Key Insights**")
default_rate=df.groupby("CODE_GENDER")["TARGET"].mean()*100
st.write(f"female Default Rate{default_rate.get('F',0):.2f}")
st.write(f"Male Default Rate {default_rate.get('M',0):.2f} ")
st.write(f'Lowest rate Gender{default_rate.idxmin()}')
st.write(f"Highest rate gender {default_rate.idxmax()}")