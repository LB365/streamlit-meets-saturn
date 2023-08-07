import datetime
import streamlit as st
from pathlib import Path
from fetch_tsa import fetch_catalog, fetch_series

st.set_page_config(
    page_title="saturn_graphs",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('saturn timeseries viewer')
HERE = Path(__file__).parent
catalog = fetch_catalog()
col1, col2 = st.columns(2)
with col1:
    options = st.multiselect(
        'Select a time series',
        catalog,
        catalog[-1]
    )
    st.write('Selected', options)
with col2:
    start_date = st.date_input(
        "start_date",
        datetime.date(2012, 1, 1)
    )
if len(options) > 0:
    data = fetch_series(options, start_date)
    st.bar_chart(data)
