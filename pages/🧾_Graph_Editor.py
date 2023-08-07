import time

import streamlit as st
import pandas as pd
from fetch_artic import (
    AC,
    artic_list_symbols,
    artic_list_versions,
    artic_read_data,
    artic_list_libraries,
    graph_types,
)

from graphs.seasonal import Seasonal
from graphs.line import Line

available_plot_types = list(set(artic_list_libraries()).intersection(graph_types))

SEASONAL_COLS = list(Seasonal.column_types.keys())

PLOT_TYPES = {
    'seasonal': Seasonal,
    'line': Line,
}

tab_edit, tab_view, tab_delete = st.tabs([
    '📋 Graph Editor',
    '📊 Graph Viewer',
    '🗑 Graph Deletion'
])

COL_RATIO = [0.15, 0.85]


def push_config_safely_to_artic_db(
        artic_db_instance,
        graph_name,
        edited_df,
        plot_type,
        validation_function
):
    if st.button('Push!'):
        if edited_df.shape[0] > 0:
            validated, errors = validation_function(edited_df)
            if validated:
                artic_db_instance[plot_type].write(graph_name, edited_df)
                st.success('Done!', icon="✅")
            else:
                st.warning('Input not valid!', icon="⚠️")
                st.write(errors)


with tab_edit:
    st.text('Creating a graph config, select a plot type')
    col_radio, col_rest = st.columns(COL_RATIO)
    with col_radio:
        plot_type = st.radio(
            "Plot type",
            available_plot_types,
        )
    with col_rest:
        if st.checkbox('New graph ?', value=False):
            # New graph doesn't require a db read, we create a blank DataFrame
            graph_name = st.text_input('Naming the graph')
            df = pd.DataFrame(columns=PLOT_TYPES[plot_type].column_types.keys())
            _edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                hide_index=True,
                key='new_editor',
                use_container_width=True,
                column_config=PLOT_TYPES[plot_type].column_types
            )
            edited_df = pd.DataFrame.from_records(st.session_state['new_editor']['added_rows'])
            st.write(edited_df.to_dict(orient='records'))
            push_config_safely_to_artic_db(
                artic_db_instance=AC,
                graph_name=graph_name,
                edited_df=edited_df,
                plot_type=plot_type,
                validation_function=PLOT_TYPES[plot_type].validation_function
            )

        else:
            graphs = artic_list_symbols(plot_type)
            graph_name = st.multiselect(
                'Editing the graph',
                graphs,
                max_selections=1
            )
            if len(graph_name) > 0:
                versions = artic_list_versions(plot_type, graph_name[0])
                version_names = [*versions.keys()]
                if len(version_names) > 1:
                    version = st.select_slider("versions", options=version_names)
                else:
                    version = version_names[-1]
                this_version = versions[version].date.strftime("%Y-%m-%d-%H:%M")
                st.write(f"Timestamp: {this_version}")
                if version is not None:
                    data = artic_read_data(
                        plot_type,
                        graph_name[0],
                        as_of=versions[version].date
                    )
                    _edited_df = st.data_editor(
                        data,
                        num_rows="dynamic",
                        hide_index=True,
                        key='patch_editor',
                        use_container_width=True,
                    )
                    st.write(_edited_df.to_dict(orient='records'))
                    push_config_safely_to_artic_db(
                        artic_db_instance=AC,
                        graph_name=graph_name[0],
                        edited_df=pd.DataFrame.from_records(_edited_df.to_dict(orient='records')),
                        plot_type=plot_type,
                        validation_function=PLOT_TYPES[plot_type].validation_function
                    )

with tab_view:
    st.text('Viewing a chart')
    col_radio, col_rest = st.columns(COL_RATIO)
    with col_radio:
        plot_type_view = st.radio(
            "Plot type view",
            available_plot_types
        )
    graphs_view = artic_list_symbols(plot_type_view)
    with col_rest:
        graph_name_view = st.multiselect('Viewing the graph', graphs_view, max_selections=1)
    if len(graph_name_view) > 0:
        data = artic_read_data(plot_type_view, graph_name_view[0])
        with st.spinner('Plotting...'):
            time.sleep(1)
        if plot_type_view == 'seasonal':
            plotter = Seasonal.plot_function(
                title=data['title'].tolist()[0],
                series=data['series_name'].tolist(),
                cut_off=int(data['cut_off'].tolist()[0]),
                start_date=data['ts_start'].tolist()[0],
                end_date=data['ts_end'].tolist()[0],
                verbose=bool(data['verbose'].tolist()[0]),
                folded=bool(data['folded'].tolist()[0]),
                precision=int(data['precision'].tolist()[0])
            )
        elif plot_type_view == 'line':
            plotter = Line.plot_function(
                title=data['title'].tolist()[0],
                series=data['series_name'].tolist(),
                labels=data['labels'].tolist(),
                start_date=data['ts_start'].tolist()[0],
                end_date=data['ts_end'].tolist()[0],
                precision=int(data['precision'].tolist()[0])
            )
        st.text("Config being plotted")
        st.write(data.T)

with tab_delete:
    st.text('Deleting a chart')
    col_radio, col_rest = st.columns(COL_RATIO)
    with col_radio:
        plot_type_delete = st.radio(
            "Plot type delete",
            available_plot_types
        )
    graphs_view = artic_list_symbols(plot_type_delete)
    with col_rest:
        graph_name_deletes = st.multiselect('Deleting the graphs', graphs_view)
    if st.button('Delete?'):
        for graph_to_delete in graph_name_deletes:
            AC[plot_type].delete(graph_to_delete)
        st.text('Deleted:')
        st.write(graph_to_delete)
