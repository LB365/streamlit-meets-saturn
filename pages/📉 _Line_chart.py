from viz.fetch_tsa import fetch_catalog
import datetime
import streamlit as st
from viz.graphs.line import (
    plot_lines,
)

from viz.graphs import COL_RATIO


def manual_lines_plot():
    catalog = fetch_catalog()
    col1, col2 = st.columns(COL_RATIO)
    with col1:
        start_date = st.date_input(
            "date_start",
            datetime.date(2012, 1, 1)
        )
    with col2:
        options = st.multiselect(
            'Select a time series for a line chart graph',
            catalog,
            catalog[-1]
        )
    if len(options) > 0:
        plot_lines(
            options,
            options,
            start_date=f'(date "{start_date:%Y-%m-%d}")'
        )
    st.write('Selected', options)


plot = manual_lines_plot()
