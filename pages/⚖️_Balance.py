from viz.moments import evaluate_not_none
import streamlit as st
import time
from viz.fetch_arctic import (
    artic_list_symbols,
    artic_read_data
)
from viz.graphs.pipe_args import pipe_args_in_plot_method

pretty_freq = {
    'Month': 'MS',
    'Quarter': 'Q',
    'Week': 'W-FRI',
    'Year': 'A',
    # 'Day': 'D',
}


def manual_balance_plot():
    plot_type_view = 'balance'
    col1, col2, col3, col4 = st.columns([0.3, 0.15, 0.15, 0.4])
    graphs_view = artic_list_symbols(plot_type_view)
    with col1:
        graph_name_view = st.multiselect(
            'Viewing the balance',
            graphs_view,
            max_selections=1
        )
    with col2:
        begins = evaluate_not_none("(monthstart (deltamonths (today) -10))")
        starts = st.date_input('Begins', value=begins)
    with col3:
        finishes = evaluate_not_none("(deltadays (yearend (today)) 1)")
        ends = st.date_input('Ends', value=finishes)
    with col4:
        _freq = st.radio('Frequency', pretty_freq.keys(), horizontal=True)
    if len(graph_name_view) > 0:
        data = artic_read_data(plot_type_view, graph_name_view[0])
        with st.spinner('Plotting...'):
            time.sleep(1)
        data = pipe_args_in_plot_method(
            data,
            plot_type_view,
            freq=pretty_freq[_freq],
            start_date=f'(date "{starts:%Y-%m-%d}")',
            end_date=f'(date "{ends:%Y-%m-%d}")',
        )


plot = manual_balance_plot()
