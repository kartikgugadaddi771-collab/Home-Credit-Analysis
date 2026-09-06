import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


from utils.data_loader import load_data
from utils.charts import histogram_chart



st.title("9. Income vs Credit")
st.markdown("Purpose")
st.write("Determine whether customers are taking loans proportional to their income")


df=load_data()

c1,c2,c3=st.columns(3)
df["Average_Credit_to_Income_Ratio"]=df["AMT_CREDIT"]/ df["AMT_INCOME_TOTAL"]
average_ratio=df["Average_Credit_to_Income_Ratio"].mean()

c1.metric("Average Credit-to-Income Ratio",f"{average_ratio:,.2f}")

highest_credit=df["AMT_CREDIT"].max()
highest_credit_income_ratio=highest_credit/df["AMT_INCOME_TOTAL"].max()
c2.metric("Highest Credit-to-Income Ratio",f"{highest_credit_income_ratio:,.2f}")

df["credit_to_income_ratio"]=df["AMT_CREDIT"]/df["AMT_INCOME_TOTAL"]
high_ratio_threshold= df["credit_to_income_ratio"].quantile(0.75)
high_ratio_df=df[df["credit_to_income_ratio"] >= high_ratio_threshold]
default_rate_high_ratio=(high_ratio_df["TARGET"].mean())*100
c3.metric("High Ratio Default Rate", f"{default_rate_high_ratio:.2f}")

col1,col2=st.columns(2)

with col1:
    st.subheader("1.Income vs Credit")
    fig=px.scatter(df,x="AMT_INCOME_TOTAL",y="AMT_CREDIT",title="Income vs Credit")
    st.plotly_chart(fig,use_container_width=True)

df["Credit_income_ratio"]= df["AMT_CREDIT"]/df["AMT_INCOME_TOTAL"]
ratio_99th= df["Credit_income_ratio"].quantile(0.99)
filtered_df= df[df["Credit_income_ratio"] <=ratio_99th]

with col2:
    st.subheader("2.Credit/Income Ratio Distribution")
    fig=px.histogram(filtered_df,x="Credit_income_ratio",nbins=50,marginal="box",title="Credit/Income Ratio Distribution")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)

df["credit_income_ratio"] = df["AMT_CREDIT"]/df["AMT_INCOME_TOTAL"]
labels=["Low","Moderate","High","Very high"]
df["Ratio_group"]= pd.qcut(df["credit_income_ratio"].dropna(), q=4, labels=labels)

group_df=df.groupby("Ratio_group", as_index=False)["TARGET"].mean()
group_df["Default_rate%"]=group_df["TARGET"]*100

with col3:
    fig=px.bar(group_df,x="Ratio_group",y="Default_rate%",title="Default Rate vs Credit_Income Ratio",
               color="Default_rate%")
    st.plotly_chart(fig,use_container_width=True)

df["credit_income_ratio"]=df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
ratio_99th=df["credit_income_ratio"].quantile(0.99)
filtered_df=df[df["credit_income_ratio"] <= ratio_99th]

with col4:
    st.subheader("4.Gender-wise Credit/Income Ratio")
    fig=px.box(filtered_df,x="CODE_GENDER",y="credit_income_ratio",title="Gender-wise Credit/Income Ratio")
    st.plotly_chart(fig,use_container_width=True)


df["credit_income_ratio"]=df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
ratio_99th=df["credit_income_ratio"].quantile(0.99)
filtered_df=df[df["credit_income_ratio"] <= ratio_99th]


st.subheader("4.Education-wise Credit/Income Ratio")
fig=px.box(filtered_df,x="NAME_EDUCATION_TYPE",y="credit_income_ratio",title="Education-wise Credit/Income Ratio")
st.plotly_chart(fig,use_container_width=True)
    
