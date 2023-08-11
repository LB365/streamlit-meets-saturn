from viz.graphs.balances.blueprint import table_to_html_for_jinja
import streamlit as st
from viz.fetch_tsa import fetch_catalog, fetch_series
from viz.graphs import Plot
from streamlit.components.v1 import html

BALANCE_COLS_DICT = {
    'series_id': st.column_config.TextColumn(
        width="large",
    ),
    'label': st.column_config.TextColumn(
        width="large",
    ),
    'level': st.column_config.NumberColumn(
    ),
    'parent': st.column_config.TextColumn(
    ),
    'last_series': st.column_config.TextColumn(
    ),
    'precision': st.column_config.TextColumn(
    ),
    'parent_agg': st.column_config.TextColumn(
    ),
    'freq_agg': st.column_config.TextColumn(
    ),
    'tol_diff': st.column_config.NumberColumn(
    ),
    'parent_coeff': st.column_config.NumberColumn(
    ),
}


def validate(df):
    return True, df


def plot_documentation():
    return ""


def plot_table(
        config,
        freq: str = None,
        start_date: str = None,
        end_date: str = None):
    freq = freq or "MS"
    end_date = end_date or "(yearend (today))"
    start_date = start_date or "(yearstart (today))"
    series = config['series_id'].tolist()
    data = fetch_series(series)
    computed_data, jinja_html = table_to_html_for_jinja(
        data,
        config,
        freq,
        start_date,
        end_date
    )
    html(jinja_html)
    return computed_data


Balance = Plot(BALANCE_COLS_DICT, plot_table, validate, plot_documentation)
