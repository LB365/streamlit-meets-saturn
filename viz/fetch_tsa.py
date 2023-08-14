import os

import streamlit as st
import pandas as pd
from tshistory.api import timeseries
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('tsa_url')
TSA = timeseries(URL)

@st.cache_data(ttl=60)  # Every hour
def fetch_catalog():
    catalog = TSA.catalog()
    return pd.DataFrame(*catalog.values()).iloc[:, 0].tolist()

def _fetch_series(series_names, start=None, end=None):
    from_value_date = pd.Timestamp(start) if start is not None else None
    to_value_date = pd.Timestamp(end) if end is not None else None
    series = map(
        lambda x: TSA.get(
            x,
            from_value_date=from_value_date,
            to_value_date=to_value_date,
        ), series_names)
    return pd.concat(series, axis=1)[from_value_date:to_value_date]


@st.cache_data(ttl=15)
def fetch_series(series_names, start=None, end=None):
    return _fetch_series(series_names, start, end)

@st.cache_data(ttl=60 * 5)
def big_fetch_series(series_names, start=None, end=None):
    return _fetch_series(series_names, start, end)