from viz.fetch_tsa import fetch_catalog
import datetime
import streamlit as st
from viz.graphs.balance import (
    plot_table,
)

from viz.graphs import COL_RATIO


def manual_balance_plot():
    catalog = fetch_catalog()
    col1, col2 = st.columns(COL_RATIO)
    with col1:
        options = st.multiselect(
            'Select a time series for a line chart graph',
            catalog,
            catalog[-1]
        )
        start_date = st.date_input(
            "Start date for line chart",
            datetime.date(2012, 1, 1)
        )
    with col2:
        if len(options) > 0:
            start_date_str = start_date.strftime('%Y-%m-%d')
            plot_lines(options, options, start_date=f'(date "{start_date_str}")')
    st.write('Selected', options)


plot = manual_lines_plot()
