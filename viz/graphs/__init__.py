from collections import namedtuple
Plot = namedtuple(
    'Plots', field_names=[
        'column_types',
        'plot_function',
        'validation_function',
        'plot_documentation'
    ]
)


COL_RATIO = [0.15, 0.85]
