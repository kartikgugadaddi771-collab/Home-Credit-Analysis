import streamlit as st


def apply_sidebar_filters(df):
    """Common sidebar filters applicable across all dashboard pages."""
    st.sidebar.header("Global Filters")

    # 1. Target Filter (Loan Default Status)
    target_opt = st.sidebar.selectbox(
        "Default Status",
        options=["All", "Repaid (0)", "Defaulted (1)"],
        index=0,
    )
    if target_opt == "Repaid (0)":
        df = df[df["TARGET"] == 0]
    elif target_opt == "Defaulted (1)":
        df = df[df["TARGET"] == 1]

    # 2. Contract Type Filter
    if "NAME_CONTRACT_TYPE" in df.columns:
        contract_opts = st.sidebar.multiselect(
            "Contract Type",
            options=df["NAME_CONTRACT_TYPE"].dropna().unique(),
            default=df["NAME_CONTRACT_TYPE"].dropna().unique(),
        )
        df = df[df["NAME_CONTRACT_TYPE"].isin(contract_opts)]

    # 3. Gender Filter
    if "CODE_GENDER" in df.columns:
        gender_opts = st.sidebar.multiselect(
            "Gender",
            options=df["CODE_GENDER"].dropna().unique(),
            default=df["CODE_GENDER"].dropna().unique(),
        )
        df = df[df["CODE_GENDER"].isin(gender_opts)]

    # 4. Income Range Slider
    if "AMT_INCOME_TOTAL" in df.columns:
        min_inc = float(df["AMT_INCOME_TOTAL"].min())
        max_inc = float(df["AMT_INCOME_TOTAL"].max())
        selected_income = st.sidebar.slider(
            "Income Range",
            min_value=min_inc,
            max_value=max_inc,
            value=(min_inc, max_inc),
        )
        df = df[
            (df["AMT_INCOME_TOTAL"] >= selected_income[0])
            & (df["AMT_INCOME_TOTAL"] <= selected_income[1])
        ]

    return df