import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from utils.data_loader import load_data
from utils.charts import histogram_chart

st.title("6.Income Analysis")

df=load_data()

st.markdown("How Does Applicant Income link to Default Risk")

df=load_data()

c1,c2=st.columns(2)
Total_Income= (df["AMT_INCOME_TOTAL"]).sum()
c1.metric("Total Income",f"{Total_Income}")

Avg_Income= (df["AMT_INCOME_TOTAL"]).mean()
c2.metric("Average Income",f"{Avg_Income:.2f}")

c3,c4=st.columns(2)
Median_Income= (df["AMT_INCOME_TOTAL"]).median()
c3.metric("Median Income",f"{Median_Income:.2f}")
Max_Income= (df["AMT_INCOME_TOTAL"]).max()
c4.metric("Max Income",f"{Max_Income:.2f}")


col1,col2=st.columns(2)

with col1:
    st.subheader("1.Income Distribution")
    st.plotly_chart(histogram_chart(df, "AMT_INCOME_TOTAL","Distribution of Applicant Income"))
    st.caption("Most applicants earn between 100k to 300k")

with col2:
    st.subheader("2. Income vs Credit")
    fig=px.bar(df,x="AMT_INCOME_TOTAL", y="AMT_CREDIT",title="Income vs Credit")
    st.plotly_chart(fig, use_container_width=True)

col3,col4=st.columns(2) 

with col3: 
    st.subheader("3.Income vs Annuity")
    fig=px.bar(df,x="AMT_INCOME_TOTAL",y="AMT_ANNUITY",title="Income vs Annuity")
    st.plotly_chart(fig,use_container_width=True) 

with col4:
    st.subheader("4.Income vs Education")
    fig=px.box(df,x="AMT_INCOME_TOTAL",y="NAME_EDUCATION_TYPE",title="Income by Education")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)

with col5:
    st.subheader("5.Income by Occupation")
    fig=px.bar(df,x="AMT_INCOME_TOTAL",y="OCCUPATION_TYPE",title="Income by Occupation",orientation="h")
    st.plotly_chart(fig,use_container_width=True)

bins=[0,50000,100000,150000,200000,300000,500000,np.inf]
labels=[
    "Below 50K",
    "50K-100K",
    "100K-150K",
    "150K-200K",
    "200K-300K",
    "300K-500K",
    "Above 500K",
    ]
df["Income_Group"]= pd.cut(df["AMT_INCOME_TOTAL"],bins=bins, labels=labels,right=False)

with col6:
    st.subheader("Default Rate by Income Group")
    fig=px.bar(df,x="Income_Group",y="TARGET",title="Default Rate by Income Group")
    st.plotly_chart(fig,use_container_width=True)