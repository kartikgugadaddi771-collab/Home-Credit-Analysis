import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from utils.data_loader import load_data
from utils.charts import histogram_chart, bar_chart


st.title("9.Annuity Burden")
st.markdown("Purpose")
st.write("Understand the repayment burden relative to customer income.")

df=load_data()

col1,col2=st.columns(2)

with col1:
    st.subheader("1.Annuity-to-Income Distribution")
    df["Annuity-to-Income Distribution"]=df["AMT_ANNUITY"]/df["AMT_INCOME_TOTAL"]
    fig= histogram_chart(df,column="Annuity-to-Income Distribution",title="Annuity-to-Income Distribution",)
    st.plotly_chart(fig,use_container_width=True)

bins=[0,0.10,0.20,0.30,np.inf]
labels=[
    "Low Repayment Burden",
    "Medium Repayment Burden",
    "High Repayment Burden",
    "Very High Repayment Burden"
]

df["Annuity-to-Income Distribution"]=df["AMT_ANNUITY"]/df["AMT_INCOME_TOTAL"]
df["Risk_group"] = pd.cut(df["Annuity-to-Income Distribution"],bins=bins,labels=labels,right=False)
default_df = (
    df.groupby("Risk_group", observed=False)["TARGET"]
    .mean()
    .reset_index(name="Default_rate")
)
default_df["DEFAULT_RATE_PCT"] = default_df["Default_rate"] * 100

with col2:
    st.subheader("2.Default Rate by Ratio")
    fig = bar_chart(
        default_df,
        group_col="Risk_group",
        value_col="DEFAULT_RATE_PCT",
        title="Default Rate by Annuity-to-Income Ratio",
    )
    st.plotly_chart(fig,use_container_width=True) 

col3,col4=st.columns(2)

df["Annuity-to-Income Distribution"]=df["AMT_ANNUITY"]/df["AMT_INCOME_TOTAL"]
with col3:
    st.subheader("3.Ratio by Gender")
    fig=px.box(df,x="CODE_GENDER",y="Annuity-to-Income Distribution",title="Annuity-to-Income Distribution")
    st.plotly_chart(fig,use_container_width=True)

with col4:
    st.subheader("4.Ratio by Income Type")
    fig=px.bar(df,x="NAME_INCOME_TYPE",y="Annuity-to-Income Distribution",title="Ratio by Income Type")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)


df["Annuity-to-Income Distribution"]=df["AMT_ANNUITY"]/df["AMT_INCOME_TOTAL"]
with col5:
    st.subheader("5.Ratio by Education")
    fig=px.bar(df,x="NAME_EDUCATION_TYPE",y="Annuity-to-Income Distribution",title="Ratio by Education")
    st.plotly_chart(fig,use_container_width=True)

with col6:
    st.subheader("6.Ratio vs TARGET")
    fig=px.pie(df,names="Annuity-to-Income Distribution",values="TARGET",title="Ratio vs TARGET")
    st.plotly_chart(fig,use_container_width=True)








