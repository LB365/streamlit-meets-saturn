import os

import streamlit as st
import pandas as pd
from tshistory.api import timeseries
from dotenv import load_dotenv
load_dotenv()
TSA = timeseries(os.getenv('tsa_url'))
CATALOG = TSA.catalog()
catalog = pd.DataFrame(*CATALOG.values())


@st.cache_data(ttl=60 * 60)  # Every hour
def fetch_catalog():
    catalog = TSA.catalog()
    return pd.DataFrame(*catalog.values()).iloc[:, 0].tolist()


@st.cache_data(ttl=15)
def fetch_series(series_names, start=None, end=None):
    from_value_date = pd.Timestamp(start) if start is not None else None
    to_value_date = pd.Timestamp(end) if end is not None else None
    series = map(
        lambda x: TSA.get(
            x,
            from_value_date=from_value_date,
            to_value_date=to_value_date,
        ), series_names)
    return pd.concat(series, axis=1)[from_value_date:to_value_date]
