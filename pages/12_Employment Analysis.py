import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.charts import histogram_chart
from utils.data_loader import load_data


st.title("12. Employment Analysis")
st.markdown("Purpose")
st.write("Understand how employment status and work history affect credit risk")

df=load_data()

c1,c2=st.columns(2)
average_employment_years=(df["DAYS_EMPLOYED"].abs() / 365).mean()
c1.metric("Average Employment Years",f"{average_employment_years:.2f}")


Most_Common_Occupation=df["OCCUPATION_TYPE"].mode()[0]
occ_count=df["OCCUPATION_TYPE"].value_counts().max()
c2.metric(label="Most Common Occupation",value=Most_Common_Occupation,delta=f"{occ_count}Applicants")

c3,c4=st.columns(2)

Most_Common_Income_Type=df["NAME_INCOME_TYPE"].mode()[0]
Income_count=df["NAME_INCOME_TYPE"].value_counts().max()
c3.metric(label="Most Common Income Type",value=Most_Common_Income_Type,delta=f"{Income_count}Types")


Highest_Risk_occupation=df.groupby("OCCUPATION_TYPE")["TARGET"].mean().idxmax()
Highest_Risk_rate=df.groupby("OCCUPATION_TYPE")["TARGET"].mean().max()*100
c4.metric(label="Highest Risk occupation",value=Highest_Risk_occupation,delta=f"{Highest_Risk_rate:,.2f}default rate",delta_color="inverse")

col1,col2=st.columns(2)

emp_years=(df["DAYS_EMPLOYED"].replace(365243,np.nan).abs().div(365).dropna())

with col1:
    st.subheader("1.Employment Years Distribution")
    fig=px.histogram(emp_years,x="DAYS_EMPLOYED",title="Employment Years Distribution")
    st.plotly_chart(fig,use_container_width=True)


    df["emp_years"]=(df["DAYS_EMPLOYED"].replace(365243,np.nan).abs().div(365))
    df["EMP_GROUP"]=pd.cut(df["emp_years"],bins=[0,2,5,10,20,np.inf],labels=["<2","2-5","5-10","10-20","20+"])
    data=df.groupby("EMP_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index()
with col2:
    st.subheader("2.Default Rate by Education")
    fig=px.bar(data,x="EMP_GROUP",y="TARGET",title="Default Rate by Education")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)

data=df["NAME_INCOME_TYPE"].value_counts().reset_index()
with col3:
    st.subheader("3.Application by Income Type")
    fig=px.density_heatmap(data,x="NAME_INCOME_TYPE",y="count",title="Application by Income Type")
    st.plotly_chart(fig,use_container_width=True)

data=df.groupby("NAME_INCOME_TYPE")["TARGET"].mean().mul(100).reset_index()
with col4:
    st.subheader("4.Default Rate by Income Type")
    fig=px.pie(data,names="NAME_INCOME_TYPE",values="TARGET",title="Default Rate by Income Type")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)

data=df["OCCUPATION_TYPE"].value_counts().reset_index()
with col5:
    st.subheader("5.Applications by Occupation")
    fig=px.density_heatmap(data,x="OCCUPATION_TYPE",y="count",title="Applications by Occupation")
    st.plotly_chart(fig,use_container_width=True)


data=df.groupby("OCCUPATION_TYPE")["TARGET"].mean().mul(100).reset_index()
with col6:
    
    st.subheader("6.Default Rate by Occupation")
    fig=px.pie(data,names="OCCUPATION_TYPE",values="TARGET",title="Default Rate by Occupation")
    st.plotly_chart(fig,use_container_width=True)

data=df.groupby("ORGANIZATION_TYPE")["TARGET"].mean().mul(100).reset_index()
st.subheader("7.Default Rate by Organization Type")
fig=px.pie(data,names="ORGANIZATION_TYPE",values="TARGET",title="Default Rate by Organization Type")
st.plotly_chart(fig,use_container_width=True)


