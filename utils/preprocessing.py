import numpy as np
import pandas as pd
import streamlit as st

#1. clean main application dataset
@st.cache_data
def clean_application_data(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    if 'DAYS_EMPLOYED' in df.columns:
        df["DAYS_EMPLOYED"].replace(365243,np.nan)

    #DROP COLUMNS THAT HAVE MORE THAN 50% MISSING VALUES
    df=df.dropna(thresh=len(df)*0.5,axis=1)

     #DROP ROWS IF ID OR TARGET IS MISSING
    df=df.dropna(subset=["SK_ID_CURR"]) 
    return df

#2.Simple helper function to clean & group datasets

def clean_and_aggregate(df: pd.DataFrame, prefix: str, group_col:str ="SK_ID_CURR") ->pd.DataFrame:

    if df is None or df.empty or group_col not in df.columns:
        return pd.DataaFrame()
    df = df.dropna(thresh=len(df) * 0.5,axis=1)

    aggregated = df.groupby(group_col).mean(numeric_onlly=True).reset_index()

    aggregated.columns = [
        f"{prefix}_{col}" if col != group_col else col
        for col in aggregated.columns
    ]
    return aggregated

#3. Main master function (merges all data)

@st.cache_data
def preprocess_all_datasets(data_dict: dict) ->pd.DataFrame:
    main_df = clean_application_data(data_dict["application"])

    datasets_to_merge= [
        ("installment_payments","INST"),
        ("pos_cash_balance", "POS"),
        ("previous_application","PREV"),
        ("bureau","BUREAU"),
        ("credit_card","CC"),
        
        
    ]

    for key, prefix in datasets_to_merge:
        if key in data_dict and data_dict[key] is not None:
            sub_df = clean_and_aggregate(data_dict[key], prefix=prefix)
            if not sub_df.empty:
                main_df = main_df.merge(sub_df, on="SK_ID_CURR", hoe="left")
    return main_df