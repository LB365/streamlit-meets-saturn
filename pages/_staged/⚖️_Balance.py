import streamlit as st
import time
from viz.fetch_arctic import (
    artic_list_symbols,
    artic_read_data
)
from viz.graphs.pipe_args import pipe_args_in_plot_method
from viz.graphs import COL_RATIO

pretty_freq = {
    'Monthly': 'MS',
    'Quarterly': 'Q',
    'Weekly': 'W-FRI',
    'Yearly': 'A',
    'Daily':'D',
}

def manual_balance_plot():
    plot_type_view = 'balance'
    col_radio, col_rest = st.columns(COL_RATIO)
    with col_radio:
        graphs_view = artic_list_symbols(plot_type_view)
        graph_name_view = st.multiselect(
            'Viewing the balance',
            graphs_view,
            max_selections=1
        )
        _freq = st.radio('frequency', pretty_freq.keys())
    with col_rest:
        if len(graph_name_view) > 0:
            data = artic_read_data(plot_type_view, graph_name_view[0])
            with st.spinner('Plotting...'):
                time.sleep(1)
            data = pipe_args_in_plot_method(
                data,
                plot_type_view,
                freq=pretty_freq[_freq],
            )



plot = manual_balance_plot()
