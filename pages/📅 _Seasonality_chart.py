from fetch_tsa import fetch_catalog
import datetime
import streamlit as st
from graphs.seasonal import (
    plot_seasonal,
    CUTOFF_YEARS
)


def manual_seasonal_plot():
    catalog = fetch_catalog()
    col1, col2 = st.columns(2)
    with col1:
        series = st.multiselect(
            'Select tickers to sum',
            catalog,
            format_func=lambda x: x,
        )
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
