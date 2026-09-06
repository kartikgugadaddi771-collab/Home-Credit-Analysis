import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px


from utils.data_loader import load_data
from utils.charts import histogram_chart


st.title("8.Annuity Analysis")
st.markdown("Purpose")
st.write("Study customers' annual loan payment obligations")

df=load_data()

c1,c2=st.columns(2)
Max_Annuity=(df["AMT_ANNUITY"]).max()
c1.metric("Max Credit",F"{Max_Annuity:,.2f}")

Avg_Annuity=(df["AMT_ANNUITY"]).mean()
c2.metric("Avg Annuity",f"{Avg_Annuity:,.2f}")


c3,c4=st.columns(2)
Median_Annuity=(df["AMT_ANNUITY"]).median()
c1.metric("Median Annuity",F"{Median_Annuity:,.2f}")

Avg_Annuity_defaulter=df[df["TARGET"]==1]["AMT_ANNUITY"].mean()
c2.metric("Avg Credit",f"{Avg_Annuity_defaulter:,.2f}")

col1,col2=st.columns(2)

with col1:
    st.subheader("1.Annuity Distribution")
    st.plotly_chart(histogram_chart(df,"AMT_ANNUITY","Distribution of Applicant ANNUITY"))

with col2:
    st.subheader("2.Annuity by TARGET")
    fig=px.bar(df,x="AMT_ANNUITY",y="TARGET",title=" Annuity by TARGET",orientation="h")
    st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)

with col3:
    
    st.subheader("3.Average Annuity by Income Type")
    fig=px.box(df,x="AMT_ANNUITY",y="NAME_INCOME_TYPE",title="Annuity vs Income Type")
    st.plotly_chart(fig,use_container_width=True)

with col4:
    
        st.subheader("4.Annuity vs Credi")
        fig=px.scatter(df,x="AMT_ANNUITY",y="AMT_CREDIT",title="Annuity vs Credi")
        st.plotly_chart(fig,use_container_width=True)
col5,col6=st.columns(2)

with col5:
     
    st.subheader("5.Annuity vs Income")
    fig=px.density_heatmap(df,x="AMT_ANNUITY",y="AMT_INCOME_TOTAL",title="Annuity vs Income")
    st.plotly_chart(fig,use_container_width=True)

# --- Grouping Data ---
labels = ["Low", "Medium", "High", "very High"]
df["ANNUITY_GROUP"] = pd.qcut(df["AMT_ANNUITY"].dropna(), q=4, labels=labels)

# Calculate average default rate
annuity_df = df.groupby("ANNUITY_GROUP", as_index=False)["TARGET"].mean()

# --- Chart 5: Default Rate by Annuity Group ---
with col6:
    st.subheader("5. Default Rate by Annuity Group")
    fig = px.bar(
        annuity_df, 
        x="ANNUITY_GROUP", 
        y="TARGET", 
        title="Default Rate by Annuity Group",
        labels={'TARGET': 'Default Rate', 'ANNUITY_GROUP': 'Annuity Group'}
    )
    st.plotly_chart(fig, use_container_width=True, key="unique_key_default_rate_82")