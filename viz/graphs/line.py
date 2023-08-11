import altair as alt
import streamlit as st
from viz.moments import evaluate_not_none
from viz.fetch_tsa import fetch_catalog, fetch_series
import pandas as pd
from viz.graphs import Plot


def validate(df):
    return True, df


def plot_documentation():
    return ""


LINES_COLS_DICT = {
    'title': st.column_config.TextColumn(
    ),
    'series_name': st.column_config.SelectboxColumn(
        options=fetch_catalog(),
        width="large",
    ),
    'labels': st.column_config.TextColumn(
    ),
    'ts_start': st.column_config.TextColumn(
        label="Start date to plot",
    ),
    'ts_end': st.column_config.TextColumn(
        label="End date to plot",
    ),
    'precision': st.column_config.NumberColumn(
        "precision",
        help="Data rounding",
        min_value=0,
        max_value=10,
        step=1,
        format="%d",
    ),
}


def plot_lines(
        series: list[str],
        labels: list[str],
        title: str = "",
        start_date: str = None,
        end_date: str = None,
        precision: int = None
):
    if series is not None:
        end_date = evaluate_not_none(
            end_date or "(yearend (today))")
        start_date = evaluate_not_none(
            start_date or "(yearstart (deltayears (today) -10)))")
        data = fetch_series(series, start=start_date, end=end_date).asfreq('D').interpolate().round(precision or 2)
        data.columns = labels
        interpolated = data.stack().reset_index()
        interpolated.columns = ['date', 'label', 'value']
        interpolated['now'] = pd.Timestamp.now().floor('D')
        base = alt.Chart(
            interpolated,
            title=alt.Title(title, anchor=alt.TitleAnchor('start')),

        )
        chart = (base.mark_line()
                 .encode(
            x=alt.X('date').title(""),
            y=alt.Y('value', scale=alt.Scale(zero=False)).title(""),
            color=alt.Color('label').title(""),
        ) + base.mark_rule(
            strokeDash=[2, 4],
            strokeWidth=0.5
        ).encode(
            x='now',
        )).interactive(bind_y=False)
        st.altair_chart(chart, use_container_width=True, theme=None)
        plot_documentation()


Line = Plot(LINES_COLS_DICT, plot_lines, validate, plot_documentation)
