import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.charts import histogram_chart
from utils.data_loader import load_data

st.title("13.Family Analysis")
st.markdown("Purpose")
st.write("Understand how employment status and work history affect credit risk")

df=load_data()

c1,c2=st.columns(2)
average_children=(df["CNT_CHILDREN"].mean())
c1.metric("Average Children",f"{average_children:.1f}")


average_family_members=(df["CNT_FAM_MEMBERS"].mean())
c2.metric("Average Family Members",f"{average_family_members:.1f}")

with_children=(df["CNT_CHILDREN"] > 0).mean()*100
without_children=(df['CNT_CHILDREN']==0).mean()*100
high_risk_family=df.groupby("NAME_FAMILY_STATUS")['TARGET'].mean().idxmax()
high_risk_rate=(df.groupby("NAME_FAMILY_STATUS")["TARGET"].mean().max()*100)


c3,c4,=st.columns(2)
c3.metric("Customer with Childern",f"{with_children:.2f}")
c4.metric("Customer without Childern",f"{without_children:.2f}")
st.metric("Highest Risk Family Type",high_risk_family,delta=f"{high_risk_rate:2f}",delta_color="inverse")

col1,col2=st.columns(2)

customer_by_children = (df.groupby("CNT_CHILDREN").size().reset_index(name="CUSTOMER_COUNT"))
with col1:
    st.subheader("1.Customers by Number of Children")
    fig=px.bar(customer_by_children,y="CNT_CHILDREN",x="CUSTOMER_COUNT",title="Customers by Number of Children")
    st.plotly_chart(fig,use_container_width=True)


data=df.groupby("CNT_CHILDREN")["TARGET"].mean().mul(100).reset_index()
with col2:
    st.subheader("2.Default Rate by Number of Children")
    fig=px.pie(data,names="CNT_CHILDREN",values="TARGET",title="Default Rate by Number of Children")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)

data_fam=df.groupby("CNT_FAM_MEMBERS").size().reset_index(name="CUSTOMER_COUNT")
with col3: 
    st.subheader("3.Customers by Family Size")
    fig=px.bar(data_fam,x="CNT_FAM_MEMBERS",y="CUSTOMER_COUNT",title="Customers by Family Size")
    st.plotly_chart(fig,use_container_width=True)

data_fam=df.groupby("CNT_FAM_MEMBERS")["TARGET"].mean().mul(100).reset_index()
with col4:
    st.subheader("4.Default Rate by Family Size")
    fig=px.pie(data_fam,names="CNT_FAM_MEMBERS",values="TARGET",title="Default Rate by Family Size")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)
data_status=df.groupby("NAME_FAMILY_STATUS")["TARGET"].mean().mul(100).reset_index()
with col5:
    st.subheader("5.Default Rate by Family Status")
    fig=px.pie(data_status,names="NAME_FAMILY_STATUS",values="TARGET",title="Default Rate by Family Status")
    st.plotly_chart(fig,use_container_width=True)
with col6:
    st.subheader("6.Income vs Family Size")
    fig=px.density_heatmap(df,x="AMT_INCOME_TOTAL",y="CNT_FAM_MEMBERS",title="Income vs Family Size")
    st.plotly_chart(fig,use_container_width=True)

data_status=df.groupby("NAME_FAMILY_STATUS").size().reset_index(name="APPLICATION")
st.subheader("7.Applications by Family Status")
fig=px.bar(data_status,x="NAME_FAMILY_STATUS",y="APPLICATION",title="Applications by Family Status")
st.plotly_chart(fig,use_container_width=True)

