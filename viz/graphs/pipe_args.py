from viz.graphs.line import Line
from viz.graphs.seasonal import Seasonal
from viz.graphs.balance import Balance


def pipe_args_in_plot_method(data, plot_type_view):
    if plot_type_view == 'seasonal':
        plotter = Seasonal.plot_function(
            title=data['title'].tolist()[0],
            series=data['series_name'].tolist(),
            cut_off=int(data['cut_off'].tolist()[0]),
            start_date=data['ts_start'].tolist()[0],
            end_date=data['ts_end'].tolist()[0],
            verbose=bool(data['verbose'].tolist()[0]) if 'verbose' in data else None,
            folded=bool(data['folded'].tolist()[0]) if 'folded' in data else None,
            precision=int(data['precision'].tolist()[0]) if 'precision' in data else None
        )
        return plotter
    elif plot_type_view == 'line':
        plotter = Line.plot_function(
            title=data['title'].tolist()[0],
            series=data['series_name'].tolist(),
            labels=data['labels'].tolist(),
            start_date=data['ts_start'].tolist()[0],
            end_date=data['ts_end'].tolist()[0],
            precision=int(data['precision'].tolist()[0]) if 'precision' in data else None
        )
        return plotter
    elif plot_type_view == 'balance':
        plotter = Balance.plot_function(
            config=data,
        )
        return plotter
    else:
        return