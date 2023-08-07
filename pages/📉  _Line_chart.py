from fetch_tsa import fetch_catalog
import datetime
import streamlit as st
from graphs.line import (
    plot_lines,
)


def manual_lines_plot():
    catalog = fetch_catalog()
    col1, col2 = st.columns(2)
    with col1:
        options = st.multiselect(
            'Select a time series for a line chart graph',
            catalog,
            catalog[-1]
        )
        st.write('Selected', options)
        start_date = st.date_input(
            "start_date",
            datetime.date(2012, 1, 1)
        )
    with col2:
        if len(options) > 0:
            start_date_str = start_date.strftime('%Y-%m-%d')
            plot_lines(options, options, start_date=f'(date "{start_date_str}")')


plot = manual_lines_plot()
