import pandas as pd
import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.charts import histogram_chart
from utils.filters import apply_sidebar_filters

st.title("15. Contract Type Analysis")
st.markdown("purpose")
st.write("Analyze credit applications according to loan contract type")

df=load_data()
df_filtered=apply_sidebar_filters(df)

cash_loan_applcn=(df_filtered["NAME_CONTRACT_TYPE"] == "Cash loans").sum()
revolving_loan=(df_filtered["NAME_CONTRACT_TYPE"] == "Revolving loans").sum()
cash_loan_def_rate=(df_filtered[df_filtered["NAME_CONTRACT_TYPE"]=="Cash loans"]['TARGET'].mean()*100)
revolve_loan_def_rate=(df_filtered[df_filtered["NAME_CONTRACT_TYPE"]=="Revolving loans"]["TARGET"].mean()*100)



c1,c2=st.columns(2)
c1.metric("CASH lOAN APPLICATIONS",f"{cash_loan_applcn}")
c2.metric("REVOLVING lOAN APPLICATIONS",f"{revolving_loan}")

c3,c4=st.columns(2)
c3.metric("CASH lOAN DEFAULT RATE",f"{cash_loan_def_rate:.2f}")
c4.metric("REVOLVING lOAN DEFAULT RATE",f"{revolve_loan_def_rate:.2f}")


col1,col2=st.columns(2)

df_contract_cnt=df["NAME_CONTRACT_TYPE"].value_counts().reset_index(name="CUSTOMER_COUNT")

with col1:
    st.subheader("1.Applications by Contract Type")
    fig=px.bar(df_contract_cnt,x="NAME_CONTRACT_TYPE",y="CUSTOMER_COUNT",title="Applications by Contract Type",text_auto=',')
    st.plotly_chart(fig,width="stretch")

def_rate_contract_type=(df.groupby("NAME_CONTRACT_TYPE")["TARGET"].mean().mul(100).reset_index())

with col2:
    st.subheader("2.Default Rate by Contract Type")
    fig2=px.bar(def_rate_contract_type,x="NAME_CONTRACT_TYPE",y="TARGET",title="Default Rate by Contract Type")
    st.plotly_chart(fig2,width="stretch")

avg_credit_by_contract_type=(df.groupby("NAME_CONTRACT_TYPE")["AMT_CREDIT"].mean().reset_index())

col3,col4=st.columns(2)

with col3:
    st.subheader("3.Average Credit by Contract Type")
    fig=px.density_heatmap(avg_credit_by_contract_type,x="NAME_CONTRACT_TYPE",y="AMT_CREDIT",title="Average Credit by Contract Type")
    st.plotly_chart(fig,width="stretch")

avg_income_by_contract_type=(df.groupby("NAME_CONTRACT_TYPE")["AMT_INCOME_TOTAL"].mean().reset_index())

with col4:
    st.subheader("4.Average Income by Contract Type")
    fig=px.density_heatmap(avg_income_by_contract_type,x="NAME_CONTRACT_TYPE",y="AMT_INCOME_TOTAL",title="Average Income by Contract Type")
    st.plotly_chart(fig,use_container_width=True)

col5,col6=st.columns(2)
avg_annuity_by_contract_type=(df.groupby("NAME_CONTRACT_TYPE")["AMT_ANNUITY"].mean().reset_index())

with col5:
    st.subheader("5.Average Annuity by Contract Type")
    fig=px.density_heatmap(avg_annuity_by_contract_type,x="NAME_CONTRACT_TYPE",y="AMT_ANNUITY",title="Average Annuity by Contract Type")
    st.plotly_chart(fig,use_container_width=True)

df["credit_income_ratio"]=df["AMT_INCOME_TOTAL"]/df["AMT_CREDIT"]
df_ratio=(df.groupby("NAME_CONTRACT_TYPE")["credit_income_ratio"].mean().reset_index())

with col6:
    st.subheader("6.Credit-to-Income Ratio by Contract Type")
    fig=px.bar(df_ratio,x="NAME_CONTRACT_TYPE",y='credit_income_ratio',title="Credit-to-Income Ratio by Contract Type",)
    st.plotly_chart(fig,use_container_width=True)