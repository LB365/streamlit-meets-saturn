import altair as alt
import streamlit as st
from moments import evaluate_not_none
from lines import HERE
from fetch import fetch_catalog, fetch_series
import pandas as pd
from graphs import Plot


def validate(df):
    return True, df


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
}


def plot_lines(
        series: list[str],
        labels: list[str],
        title: str = "",
        start_date: str = None,
        end_date: str = None
):
    if series is not None:
        end_date = evaluate_not_none(
            end_date or "(yearend (today))")
        start_date = evaluate_not_none(
            start_date or "(yearstart (deltayears (today) -10)))")
        data = fetch_series(series, start=start_date, end=end_date).asfreq('D').interpolate()
        data.columns = labels
        interpolated = data.stack().reset_index()
        interpolated.columns = ['date', 'label', 'value']
        interpolated['now'] = pd.Timestamp.now().floor('D')
        base = alt.Chart(
            interpolated,
            title=alt.Title(title, anchor=alt.TitleAnchor('start'))
        )
        chart = (base.mark_line()
                 .encode(
            x=alt.X('date').title(""),
            y=alt.Y('value').title(""),
            color=alt.Color('label').title(""),
        ) + base.mark_rule().encode(x='now')
                 ).interactive(bind_y=False)
        st.altair_chart(chart, use_container_width=True, theme=None)


Line = Plot(LINES_COLS_DICT, plot_lines, validate)
