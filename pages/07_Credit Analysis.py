import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from utils.data_loader import load_data
from utils.charts import histogram_chart,bar_chart





st.title("7.Credit Analysis")
st.markdown("Purpose")
st.write("Analyze the amount of credit requested by applicants")
df=load_data()

c1,c2=st.columns(2)
Total_credit=(df["AMT_CREDIT"]).sum()
c1.metric("Total Credit",F"{Total_credit:,.2f}")

Avg_credit=(df["AMT_CREDIT"]).mean()
c2.metric("Avg Credit",f"{Avg_credit:,.2f}")

c3,c4,c5=st.columns(3)
Median_credit=(df["AMT_CREDIT"]).median()
c3.metric("Median Credit",f"{Median_credit:,.2f}")


Max_credit=(df["AMT_CREDIT"]).max()
c4.metric("Maximum Credit",f"{Max_credit:,.2f}")


Min_credit=(df["AMT_CREDIT"]).min()
c5.metric("Minimum Credit",f"{Min_credit:,.2f}")

col1,col2=st.columns(2)

with col1:
    st.subheader("1.Credit Amount Distribution")
    st.plotly_chart(histogram_chart(df,"AMT_CREDIT","Distribution of Applicant Credit"))

with col2:
    st.subheader("2.Credit Amount by TARGET")
    fig=px.bar(df,x="AMT_CREDIT",y="TARGET",title="Credit Amount by TARGET",orientation="h")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)
with col3:
    st.subheader("3.Average Credit by Gender")
    credit_by_gender = df.groupby("CODE_GENDER", as_index=False)["AMT_CREDIT"].mean()
    fig=px.pie(df,names="CODE_GENDER",values="AMT_CREDIT",title="Average Credit by Gender")
    st.plotly_chart(fig,use_container_width=True)

with col4:
    st.subheader("4.Credit by Income Type")
    fig=px.histogram(df,x="NAME_INCOME_TYPE",y="AMT_CREDIT",title="Average Credit by Gender")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)
with col5:
    st.subheader("5.Credit by Education")
    fig=px.box(df,x="NAME_EDUCATION_TYPE",y="AMT_CREDIT",title="Credit by Education")
    st.plotly_chart(fig,use_container_width=True)

with col6:
    
    st.subheader("5.Credit by Contract Type")
    fig=px.density_heatmap(df,x="NAME_CONTRACT_TYPE",y="AMT_CREDIT",title="Credit by Contract Type")
    st.plotly_chart(fig,use_container_width=True)



bins=[0,100000,300000,500000,700000,1000000,np.inf]
labels=[
    "Below 100K",
    "100K–300K",
    "300K–500K",
    "500K–700K",
    "700K–1M",
    "Above 1M",
    ]
df["Credit Range"]=pd.cut(df["AMT_CREDIT"],bins=bins,labels=labels,right=False)


st.subheader("Default Rate by Credit Range")
fig=px.bar(df,x="Credit Range",y="TARGET",title="Default Rate by Credit Range")
st.plotly_chart(fig,use_container_width=True)