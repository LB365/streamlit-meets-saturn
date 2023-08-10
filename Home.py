import datetime
import streamlit as st
from pathlib import Path
from viz.fetch_tsa import fetch_catalog, fetch_series

st.set_page_config(
    page_title="saturn_graphs",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('🪐 Saturn timeseries viewer')
HERE = Path(__file__).parent
catalog = fetch_catalog()
coll,colr = st.columns([0.8, 0.2])
with coll:
    options = st.multiselect(
        'Select a time series',
        catalog,
        catalog[-1]
    )
with colr:
    start_date = st.date_input(
            "start_date",
            datetime.date(2012, 1, 1)
    )
if len(options) > 0:
    data = fetch_series(options, start_date)
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(data)
    with col2:
        st.line_chart(data)
    st.write('Selected:', options)
