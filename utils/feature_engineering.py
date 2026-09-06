import numpy as np
import pandas as pd

def create_domain_feature(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()

    #1. credit to income Ratio
    
    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["CREDIT_INCOME_PERCENT"] = df["AMT_CREDIT"] / (
            df['AMT_INCOME_TOTAL'] +1e-5
            )

    #2. Annuity to Income Ratio 
    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_INCOME_PERCENT"] = df["AMT_ANNUITY"] / (
            df["AMT_INCOME_TOTAL"]+ 1e-5
        )

    #3. Loan Term in years / Payment Duration
    if "AMT_CREDIT" in df.columns and "AMT_ANNUITY" in df.columns:
        df["CREDIT_TERM"] = df["AMT_CREDIT"] / (df["AMT_ANNUITY"] +1e-5)

    #4. Employment Duration in Years 
    if "DAYS_EMPLOYED" in df.columns:
        df["DAYS_EMPLOYED_ANOM"] = df["DAYS_EMPLOYED"]==365243
        df["DAYS_EMPLOYED_CLEAN"]= df["DAYS_EMPLOYED"].replace(
            365243,np.nan
        )
        df["EMPLOYMENT_YEARS"] = df["DAYS_EMPLOYED_CLEAN"]/ -365.25
    #5. Goods Price Ratio
    if "AMT_CREDIT" in df.columns and "AMT_GOODS_PRICE" in df.columns:
        df["GOODS_PRICE_PERCENT"] = df["AMT_CREDIT"] / (
            df["AMT_GOOFS_PRICE"] +1e-5
        )

    #6. Age in years (DAYS_BIRTH  is negative in this dataset)
    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = (df["DAYS_BIRTH"] /365.25).astype(int)

    #7. External Source Ratios (combining top predictive Scores)
    ext_cols= [c for c in ["EXT_SOURCE_1", "EXT_SOURCE_2","EXT_SOURCE_3"] if c in df.columns]
    if ext_cols:
        df["EXT_SOURCES_MEAN"] = df[ext_cols].mean(axis=1)
        df["EXT_SOURCES_MIN"] = df[ext_cols].min(axis=1)
        df["EXT_SOURCES_MAX"] = df[ext_cols].max(axis=1)
    return df