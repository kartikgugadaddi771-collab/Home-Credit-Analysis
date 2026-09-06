import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from utils.data_loader import load_data
from utils.charts import histogram_chart, bar_chart


st.title("11. Education Analysis")
st.markdown("Purpose")
st.write("Analyze applicants according to education leve")

df=load_data()

c1,c2=st.columns(2)
most_common_edu=df["NAME_EDUCATION_TYPE"].mode()[0]
c1.metric("Most coomon Education",f"{most_common_edu}")

Highest_Income_Education_Group=Highest_Income_Education_Group = (
    df.groupby("NAME_EDUCATION_TYPE")["AMT_INCOME_TOTAL"]
    .mean()
    .idxmax()
)
c2.metric("Highest Income Education Group",f"{Highest_Income_Education_Group}")

c3,c4=st.columns(2)

edu_defaults=df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean()
lowest_default_edu= edu_defaults.idxmin()
c3.metric("Lowest Default Education Group",f"{lowest_default_edu}")
highest_default_edu=edu_defaults.idxmax()
c4.metric("Highest Default Education Group",f"{highest_default_edu}")


col1,col2=st.columns(2)

with col1:
    st.subheader("1.Income by Education")
    fig=px.bar(df,x="AMT_INCOME_TOTAL",y="NAME_EDUCATION_TYPE",title="Income by EducatioN")
    st.plotly_chart(fig,use_container_width=True)

with col2:
    
    st.subheader("2.Credit by Education")
    fig=px.scatter(df,x="AMT_CREDIT",y="NAME_EDUCATION_TYPE",title="Credit by Education")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)
with col3:
    st.subheader("3.Annuity by Education")
    fig=px.scatter(df,x="AMT_ANNUITY",y="NAME_EDUCATION_TYPE",title="Annuity by Education")
    st.plotly_chart(fig,use_container_width=True)

with col4:
     st.subheader("4.Customer by Education")
     customer_by_education = (
         df["NAME_EDUCATION_TYPE"]
         .value_counts()
         .rename_axis("NAME_EDUCATION_TYPE")
         .reset_index(name="CUSTOMER_COUNT")
     )
     fig = px.bar(
         customer_by_education,
         x="NAME_EDUCATION_TYPE",
         y="CUSTOMER_COUNT",
         title="Customers by Education",
         
     )
     st.plotly_chart(fig, use_container_width=True)



credit_to_income_by_education = (
    df.assign(
        CREDIT_TO_INCOME_RATIO=df["AMT_CREDIT"]
        / df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )
     .groupby("NAME_EDUCATION_TYPE", as_index=False)["CREDIT_TO_INCOME_RATIO"]
    .mean()
)
credit_to_income_by_education["AVERAGE_RATIO_PERCENT"] = (
    credit_to_income_by_education["CREDIT_TO_INCOME_RATIO"] * 100
)

col5,col6=st.columns(2)
with col5:
    st.subheader("5. Credit-to-Income Ratio by Education")
    fig = px.bar( credit_to_income_by_education,x="NAME_EDUCATION_TYPE",y="AVERAGE_RATIO_PERCENT",title="Average Credit-to-Income Ratio by Education",)
    st.plotly_chart(fig, use_container_width=True)

labels=["Secondary Special","Higher Education","Incomplete Higher","Lower Secondary","Academic Degree"]



Education_df = df.groupby("NAME_EDUCATION_TYPE", as_index=False)["TARGET"].mean()
Education_df["DEFAULT_RATE_PCT"] = Education_df["TARGET"] * 100

with col6:
    
    st.subheader("6.Default Rate by Education")
    fig = px.bar(
        Education_df, 
        x="NAME_EDUCATION_TYPE", 
        y="DEFAULT_RATE_PCT", 
        title="Default Rate by Education",
        
    )
    st.plotly_chart(fig, use_container_width=True)



    

