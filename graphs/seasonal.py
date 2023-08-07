import datetime

import streamlit as st
import pandas as pd
import json
from moments import evaluate_not_none
from Home import HERE
from fetch import fetch_catalog, fetch_series

from graphs import Plot

CUTOFF_YEARS = [2018, 2019, 2020, 2021, 2022]

with open(HERE / 'vegalites' / 'seasonal.json') as file:
    VEGA_SEASONAL = json.load(file)

with open(HERE / 'vegalites' / 'seasonal_unfold.json') as file:
    VEGA_SEASONAL_UNFOLD = json.load(file)

SEASONAL_COLS_DICT = {
    'title': st.column_config.TextColumn(
    ),
    'series_name': st.column_config.SelectboxColumn(
        options=fetch_catalog(),
        width="large",
    ),
    'ts_start': st.column_config.TextColumn(
        label="Start date to plot",
    ),
    'ts_end': st.column_config.TextColumn(
        label="End date to plot",
    ),
    'cut_off': st.column_config.NumberColumn(
        "cut off year",
        help="Last year in the range",
        min_value=2018,
        max_value=2023,
        step=1,
        format="%d",
    ),
    'folded': st.column_config.CheckboxColumn(
        help='Is the plot x-axis from Jan to Dec',
        default=True),
    'verbose': st.column_config.CheckboxColumn(
        default=False),
    'precision': st.column_config.NumberColumn(
        "precision",
        help="Data rounding",
        min_value=0,
        max_value=10,
        step=1,
        format="%d",
    ),
}


def plot_documentation(folded, verbose):
    if verbose:
        if folded:
            st.caption(
                "Seasonality chart with the seasonal range representing the min-max values up to the cutoff year"
            )
        else:
            st.caption(
                """Seasonality unfolded chart with the seasonal range representing 
                the q1-q3 seasonal quantiles, ignoring the cutoff year"""
            )


def validate_plot_seasonal(df):
    catalog = fetch_catalog()
    in_catalog = [
        x in catalog
        for x in df['series_name'].to_list()
    ]
    ts_start_valid = [
        evaluate_not_none(x) is not None
        for x in df['ts_start'].to_list()
    ]
    ts_end_valid = [
        evaluate_not_none(x) is not None
        for x in df['ts_end'].to_list()
    ]
    errors = pd.DataFrame(
        [in_catalog, ts_end_valid, ts_end_valid],
        ['wrong series', 'wrong start', 'wrong end']
    )
    return all(in_catalog) & all(ts_end_valid) & all(ts_start_valid), errors


def plot_seasonal(
        series: list[str],
        title: str = "",
        cut_off: int = None,
        start_date: str = None,
        end_date: str = None,
        verbose: bool = True,
        folded: bool = True,
        precision: int = None,
):
    if series is not None:
        cut_off = cut_off or 2018
        end_date = evaluate_not_none(
            end_date or "(yearend (today))")
        start_date = evaluate_not_none(
            start_date or "(yearstart (deltayears (today) -10)))")
        data = fetch_series(series, start=start_date, end=end_date)
        seasonal = data.asfreq('D').interpolate().sum(axis=1)
        seasonal = seasonal.reset_index().assign(predicted=False).round(precision or 2)
        seasonal.columns = ['__0__', '__2__', '__1__']
        __seasonal_plot(
            title,
            series,
            seasonal,
            cut_off,
            VEGA_SEASONAL if folded else VEGA_SEASONAL_UNFOLD,
            verbose
        )
        plot_documentation(folded, verbose)


def __seasonal_plot(title, series, data, cut_off, specs, verbose):
    chart = st.vega_lite_chart(
        data=data,
        spec={
            "title": {
                "text": title,
                "anchor": "start"
            },
            'params': [{
                "name": "cutoff_year",
                "value": cut_off
            }],
            'transform': specs['transform'],
            'encoding': specs['encoding'],
            'layer': specs['layer']
        },
        use_container_width=True,
        theme=None,
    )
    if verbose:
        st.write(series)


Seasonal = Plot(
    SEASONAL_COLS_DICT,
    plot_seasonal,
    validate_plot_seasonal,
    plot_documentation,
)
