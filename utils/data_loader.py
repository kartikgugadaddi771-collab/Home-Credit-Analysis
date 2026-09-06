
import os
import pandas as pd
import streamlit as st

# Base path relative to project root
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _read_csv(file_name, nrows=None):
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Missing dataset: {file_path}. "
            "Create a data folder in the project root and add the required CSV file."
        )
    return pd.read_csv(file_path, nrows=nrows)


# Individual Cached Data Loaders
@st.cache_data(show_spinner="Loading application data...")
def load_application(nrows=None):
    """Loads the main application_train dataset."""
    return _read_csv("application_train.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading bureau data...")
def load_bureau(nrows=None):
    """Loads credit bureau history data."""
    return _read_csv("bureau.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading bureau balance data...")
def load_bureau_balance(nrows=None):
    """Loads bureau balance history data."""
    return _read_csv("bureau_balance.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading credit card balance data...")
def load_credit_card_balance(nrows=None):
    """Loads credit card balance history data."""
    return _read_csv("credit_card_balance.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading installment payments data...")
def load_installment_payments(nrows=None):
    """Loads installment payments history data."""
    return _read_csv("installments_payments.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading POS cash balance data...")
def load_pos_cash_balance(nrows=None):
    """Loads POS cash balance data."""
    return _read_csv("POS_CASH_balance.csv", nrows=nrows)


@st.cache_data(show_spinner="Loading previous applications data...")
def load_previous_application(nrows=None):
    """Loads previous applications data."""
    return _read_csv("previous_application.csv", nrows=nrows)


# Wrapper function required by Executive Overview / Dashboard pages
def load_data(file_name="merge_data.csv", nrows=1000):
    """
    Generic load_data function imported by sub-pages.
    Defaults to loading application_train.csv.
    """
    if file_name in {"application_train.csv", "merge_data.csv"}:
        return load_application(nrows=nrows)
    
    return _read_csv(file_name, nrows=nrows)


# Utility function to load all datasets as a dictionary
def load_all_data(nrows=1000) -> dict:
    """Returns a dictionary containing all loaded dataframes."""
    return {
        "application": load_application(nrows=nrows),
        "bureau": load_bureau(nrows=nrows),
        "bureau_balance": load_bureau_balance(nrows=nrows),
        "credit_card": load_credit_card_balance(nrows=nrows),
        "installment_payments": load_installment_payments(nrows=nrows),
        "pos_cash_balance": load_pos_cash_balance(nrows=nrows),
        "previous_application": load_previous_application(nrows=nrows),
    }