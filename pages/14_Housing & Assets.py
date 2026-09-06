import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.filters import apply_sidebar_filters
from utils.data_loader import load_data


st.title("13.Housing & Assets")
st.markdown("Purpose")
st.write("Analyze property and vehicle ownership.")

df=load_data()
df_filtered=apply_sidebar_filters(df)

car_owners=(df["FLAG_OWN_CAR"]=="Y").mean()*100
property_owners=(df["FLAG_OWN_REALTY"]=="Y").mean()*100
customers_owning_both=((df['FLAG_OWN_CAR']=="Y")&(df["FLAG_OWN_REALTY"]=="Y")).mean()*100
def_rateprop_own=df[df["FLAG_OWN_REALTY"]=="Y"]["TARGET"].mean()*100

c1,c2=st.columns(2)
c1.metric("CAR OWNERS",f"{car_owners}")
c2.metric("PROPERTY_OWNERS",f"{property_owners:.2f}")

c3,c4=st.columns(2)
c1.metric("BOTH OWNERS",f"{customers_owning_both}")
c2.metric("default rate of propeety owners",f"{def_rateprop_own:.2f}")

col1,col2=st.columns(2)
with col1:
    fig1 = px.pie(df,names="FLAG_OWN_CAR",title="Car Ownership Distribution",hole=0.4,)
    fig1.update_traces(textinfo="percent+label")
    st.plotly_chart(fig1, width="stretch")

with col2:
    fig2 = px.pie(df,names="FLAG_OWN_REALTY",title="Property Ownership Distribution",hole=0.4,)
    fig2.update_traces(textinfo="percent+label")
    st.plotly_chart(fig2, width="stretch")

col3,col4=st.columns(2)
with col3:
   df_car = (df.groupby("FLAG_OWN_CAR")["TARGET"].mean().mul(100).reset_index())
   fig3 = px.bar(df_car,x="FLAG_OWN_CAR",y="TARGET",title="Default Rate (%) by Car Ownership",text_auto=".2f")
   st.plotly_chart(fig3, width="stretch")

with col4:
    df_realty = (df.groupby("FLAG_OWN_REALTY")["TARGET"].mean().mul(100).reset_index())
    fig4 = px.bar(df_realty,x="FLAG_OWN_REALTY",y="TARGET",title="Default Rate (%) by Property Ownership",text_auto=".2f",)
    st.plotly_chart(fig4, width="stretch")

col5,col6=st.columns(2)

with col5:
    df_house_cnt = (df["NAME_HOUSING_TYPE"].value_counts().reset_index(name="CUSTOMER_COUNT"))
    fig5 = px.bar(df_house_cnt,y="NAME_HOUSING_TYPE",x="CUSTOMER_COUNT",orientation="h",title="Applicants by Housing Type",text_auto=",",)
    fig5.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig5, width="stretch")

with col6:
    df_house_risk = (df.groupby("NAME_HOUSING_TYPE")["TARGET"].mean().mul(100).reset_index())
    fig6 = px.bar(df_house_risk,y="NAME_HOUSING_TYPE",x="TARGET", orientation="h",title="Default Rate (%) by Housing Type",text_auto=".2f",)
    fig6.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig6, width="stretch")

df_house_credit = (
    df.groupby("NAME_HOUSING_TYPE")["AMT_CREDIT"].mean().reset_index()
)
fig7 = px.bar(
    df_house_credit,
    y="NAME_HOUSING_TYPE",
    x="AMT_CREDIT",
    orientation="h",
    title="Average Credit by Housing Type",
    text_auto=",.0f",
)
fig7.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig7, width="stretch")