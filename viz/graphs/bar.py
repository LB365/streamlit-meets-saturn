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


timeunits = {
    'M': 'yearmonth',
    'Q': 'yearquarter',
    'W-FRI': 'yearmonthdate',
    'D': 'yearmonthdate',
    'Y': 'year',
}

formatdate = {
    'M': '%b-%y',
    'Q': 'Q%q-%y',
    'W-FRI': '%d-%b-%y',
    'D': '%d-%b',
    'Y': '%y',
}

LINES_AND_BAR_COLS_DICT = {
    'title': st.column_config.TextColumn(
    ),
    'series_name': st.column_config.TextColumn(
        width="large",
    ),
    'labels': st.column_config.TextColumn(
    ),
    'total': st.column_config.CheckboxColumn(
        default=True
    ),
    'ts_start': st.column_config.TextColumn(
        label="Start date to plot",
    ),
    'ts_end': st.column_config.TextColumn(
        label="End date to plot",
    ),
    'order': st.column_config.SelectboxColumn(
        options=['Natural', 'Variance']
    ),
    'freq': st.column_config.SelectboxColumn(
        options=['M', 'Q', 'D', 'W-FRI', 'Y']
    ),
    'freq_agg': st.column_config.SelectboxColumn(
        options=['mean', 'sum', 'std', 'median', 'last']
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


def plot_lines_and_bar(
        series: list[str],
        labels: list[str],
        styles: list[str],
        order: str = None,
        freq: str = None,
        freq_agg: str = None,
        total: bool = True,
        title: str = "",
        start_date: str = None,
        end_date: str = None,
        precision: int = None
):
    if series is not None:
        freq = freq or "D"
        freq_agg = freq_agg or "mean"
        styles_dict = dict(zip(labels, styles))
        end_date = evaluate_not_none(
            end_date or "(yearend (today))")
        start_date = evaluate_not_none(
            start_date or "(yearstart (deltayears (today) -10)))")
        data = fetch_series(series, start=start_date, end=end_date)
        data.index = data.index.to_period(freq)
        data = data.groupby(data.index.start_time).agg(freq_agg).cumsum().round(precision or 2)
        data.columns = labels
        stacked = data.stack().reset_index()
        totals = data.sum(axis=1).reset_index()
        stacked.columns = ['date', 'label', 'value']
        totals.columns = ['date', 'value']
        stacked['now'] = pd.Timestamp.now().floor('D')
        base = alt.Chart(
            stacked,
            title=alt.Title(title, anchor=alt.TitleAnchor('start')),

        )
        base_total = alt.Chart(
            totals,
        )
        chart_total = base_total.mark_line(
            point=alt.OverlayMarkDef(filled=False, fill="white", stroke='black'), stroke='black'
        ).encode(
            x=alt.X(f'{timeunits[freq]}(date):O',
                    axis=alt.Axis(format=formatdate[freq])).title(""),
            y=alt.Y('value', scale=alt.Scale(zero=False)).title(""),
        ).interactive(bind_y=False)

        chart = (base.mark_bar(stroke='black', strokeWidth=0.3)
                 .encode(
            x=alt.X(f'{timeunits[freq]}(date):O',
                    axis=alt.Axis(format=formatdate[freq])).title(""),
            y=alt.Y('value', scale=alt.Scale(zero=False)).title(""),
            color=alt.Color('label').title(""),
        ) + base.mark_rule(
            strokeDash=[2, 4],
            strokeWidth=0.5
        ).encode(
            x=f'{timeunits[freq]}(now):O',
        )).interactive(bind_y=False)
        st.altair_chart(chart + chart_total, use_container_width=True, theme=None)
        plot_documentation()


Line = Plot(LINES_AND_BAR_COLS_DICT, plot_lines_and_bar, validate, plot_documentation)

if __name__ == '__main__':
    series_test = [
        'oil.ny_fed_report.residual.usd_bbl.weekly',
        'oil.ny_fed_report.supply.usd_bbl.weekly',
        'oil.ny_fed_report.demand.usd_bbl.weekly'
    ]

    plot_lines_and_bar(
        series=series_test,
        labels=['residual', 'supply', 'demand'],
        styles=3 * ['Bar'],
        freq='M',
        freq_agg='mean',
        # start_date='(yearstart (today))'
    )
