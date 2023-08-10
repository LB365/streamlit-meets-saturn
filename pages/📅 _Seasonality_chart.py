from viz.fetch_tsa import fetch_catalog
import datetime
import streamlit as st
from viz.graphs.seasonal import (
    plot_seasonal,
    CUTOFF_YEARS
)
from viz.graphs import COL_RATIO

def manual_seasonal_plot():
    catalog = fetch_catalog()
    series = st.multiselect(
        'Select tickers to sum',
        catalog,
        format_func=lambda x: x,
    )
    col1, col2 = st.columns(COL_RATIO)
    with col1:
        start_date_seasonal = st.date_input(
            'start_date_seasonal',
            datetime.date(2012, 1, 1)
        )
        cutoff = st.selectbox(
            'Select a cutoff year', CUTOFF_YEARS)
        folded = st.checkbox('folded', value=True)
    with col2:
        if len(series) > 0:
            start_date_str = start_date_seasonal.strftime('%Y-%m-%d')
            return plot_seasonal(
                series=series,
                cut_off=cutoff,
                start_date=f'(date "{start_date_str}")',
                folded=folded,
            )


plot = manual_seasonal_plot()
