import streamlit as st
import pandas as pd

def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculates key summary metrics from the preprocessed dataframe."""
    metrics = {}
    
    # 1. Total Applications Count
    metrics["total_applications"] = len(df)
    
    # 2. Total Loan Amount (AMT_CREDIT)
    if "AMT_CREDIT" in df.columns:
        metrics["total_credit_amount"] = df["AMT_CREDIT"].sum()
        metrics["avg_credit_amount"] = df["AMT_CREDIT"].mean()
    else:
        metrics["total_credit_amount"] = 0
        metrics["avg_credit_amount"] = 0
        
    # 3. Default Rate (TARGET column where 1 = Default, 0 = Repaid)
    if "TARGET" in df.columns:
        default_count = (df["TARGET"] == 1).sum()
        metrics["default_count"] = default_count
        metrics["default_rate"] = (default_count / len(df)) * 100
    else:
        metrics["default_count"] = 0
        metrics["default_rate"] = 0.0

    # 4. Average Income
    if "AMT_INCOME_TOTAL" in df.columns:
        metrics["avg_income"] = df["AMT_INCOME_TOTAL"].mean()
    else:
        metrics["avg_income"] = 0
        
    return metrics

def display_target_kpi_cards(df: pd.DataFrame):
    """Displays Target/Default specific KPI cards."""
    total_customers = len(df)
    target_0_count = (df['TARGET'] == 0).sum()
    target_1_count = (df['TARGET'] == 1).sum()
    
    default_rate = (target_1_count / total_customers) * 100 if total_customers > 0 else 0
    non_default_rate = (target_0_count / total_customers) * 100 if total_customers > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="TARGET = 0 Customers", value=f"{target_0_count:,}")
    with col2:
        st.metric(label="TARGET = 1 Customers", value=f"{target_1_count:,}")
    with col3:
        st.metric(label="Default Rate %", value=f"{default_rate:.2f}%")
    with col4:
        st.metric(label="Non-Default Rate %", value=f"{non_default_rate:.2f}%")


def get_kpis(df: pd.DataFrame) -> dict:
    """
    Computes key performance indicators for the Home Credit dashboard.
    Handles missing columns gracefully to avoid runtime errors.
    """
    if df is None or df.empty:
        return {
            "Total Application": "0",
            "Total default customer": "0",
            "Total non default customer": "0",
            "Default rate": "0.0%",
            "avg credit amount": "$0.00",
            "Avg Income": "$0.00",
            "Avg annuity": "$0.00",
            "Total credit": "$0.00",
        }

    total_apps = len(df)

    # 1. Default vs Non-Default Calculations
    if "TARGET" in df.columns:
        default_cust = int(df["TARGET"].sum())
        non_default_cust = total_apps - default_cust
        default_rate = round((default_cust / total_apps) * 100, 2) if total_apps > 0 else 0
    else:
        default_cust = 0
        non_default_cust = total_apps
        default_rate = 0.0

    # 2. Financial Metrics (Safely handle missing columns)
    avg_credit = round(df["AMT_CREDIT"].mean(), 2) if "AMT_CREDIT" in df.columns else 0.0
    avg_income = round(df["AMT_INCOME_TOTAL"].mean(), 2) if "AMT_INCOME_TOTAL" in df.columns else 0.0
    avg_annuity = round(df["AMT_ANNUITY"].mean(), 2) if "AMT_ANNUITY" in df.columns else 0.0
    total_credit = round(df["AMT_CREDIT"].sum(), 2) if "AMT_CREDIT" in df.columns else 0.0

    # Return dictionary with exact key names used across Streamlit pages
    return {
        "Total Application": f"{total_apps:,}",
        "Total default customer": f"{default_cust:,}",
        "Total non default customer": f"{non_default_cust:,}",
        "Default rate": f"{default_rate:.2f}%",
        "avg credit amount": f"${avg_credit:,.2f}",
        "Avg Income": f"${avg_income:,.2f}",
        "Avg annuity": f"${avg_annuity:,.2f}",
        "Total credit": f"${total_credit:,.2f}",
    }

def display_demographic_kpis(df: pd.DataFrame):
    """
    Displays Demographic KPI cards: Total Customers, Average Age, 
    Male Customers, Female Customers, and Average Family Size.
    """
    total_customers = len(df)
    
    # Calculate Age from DAYS_BIRTH (Home Credit dataset uses negative days)
    if 'DAYS_BIRTH' in df.columns:
        avg_age = abs(df['DAYS_BIRTH']).mean() / 365.25
    else:
        avg_age = 0

    # Gender counts
    male_customers = (df['CODE_GENDER'] == 'M').sum() if 'CODE_GENDER' in df.columns else 0
    female_customers = (df['CODE_GENDER'] == 'F').sum() if 'CODE_GENDER' in df.columns else 0

    # Family Size
    avg_family_size = df['CNT_FAM_MEMBERS'].mean() if 'CNT_FAM_MEMBERS' in df.columns else 0

    # Render KPI Cards in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Customers", value=f"{total_customers:,}")
    with col2:
        st.metric(label="Average Age", value=f"{avg_age:.1f} yrs")
    with col3:
        st.metric(label="Male Customers", value=f"{male_customers:,}")
    with col4:
        st.metric(label="Female Customers", value=f"{female_customers:,}")
    with col5:
        st.metric(label="Average Family Size", value=f"{avg_family_size:.1f}")

# 1. Preprocess Age & Age Groups
# 1. Age Analysis KPIs Function
def age_analysis_kpis(df: pd.DataFrame):
    df = df.copy()
    
    # Preprocess Age & Age Groups
    df['AGE'] = (df['DAYS_BIRTH'].abs() / 365).astype(int)
    bins = [18, 25, 30, 35, 40, 45, 50, 55, 60, 100]
    labels = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61+']
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=True)

    # 2. Calculate values for the 4 KPI Cards
    avg_age = df['AGE'].mean()
    youngest = df['AGE'].min()
    oldest = df['AGE'].max()
    highest_risk_group = df.groupby('AGE_GROUP', observed=False)['TARGET'].mean().idxmax()

    # 3. Render Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Age", f"{avg_age:.1f} yrs")
    c2.metric("Youngest Customer", f"{youngest} yrs")
    c3.metric("Oldest Customer", f"{oldest} yrs")
    c4.metric("Highest Risk Age Group", f"{highest_risk_group}")

