import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from utils import utc_to_local, format_title

LINE_COLOR = "#27b5b3"
SOURCES = ['VOC-CCS', 'VOC-TGS', 'PM25', 'PM10']


def get_graphs(db_wrapper, is_main_graphs=False):
    graphs = []
    if is_main_graphs:
        class_names = 'graph-div col s12'
        data = db_wrapper.get_data(limit=180)  # minute=True
    else:  # small graphs
        class_names = 'graph-div col-xs-12 col-sm-6 col-md-6 col-lg-6'
        data = db_wrapper.get_data(limit=180)

    for source in SOURCES:
        x = [utc_to_local(d['at']) for d in data]
        y = [float(d[source]) for d in data]

        trace = go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color=LINE_COLOR, width=3),
        )

        layout = get_layout(x, y)

        dcc_graph = dcc.Graph(
            id=source,
            figure={'data': [trace], 'layout': layout},
            config={'displayModeBar': False}
        )

        # title
        source_title = source
        if source == 'PM25':
            source_title = 'PM2.5'
        title = format_title(source_title, y[0]) if y else 'no data'

        # output div
        graph_div = html.Div([
            html.Div([
                html.H3(title)
            ], className='Title'),
            dcc_graph,
        ], className=class_names)

        graphs.append(graph_div)

    return graphs


def get_layout(x, y):
    min_x = min(x) if x else 0
    max_x = max(x) if x else 0
    min_y = min(y) if y else 0
    max_y = max(y) if y else 0

    return go.Layout(
        xaxis=dict(
            range=[min_x, max_x],
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                size=12,
                color='rgb(204, 204, 204)',
            )
        ),
        yaxis=dict(
            range=[min_y, max_y],
            tickcolor='rgb(204, 204, 204)',
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,

            hoverformat='.0f',
            tickfont=dict(
                size=12,
                color='rgb(204, 204, 204)',
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=370,
        margin=go.layout.Margin(
            t=30,
            l=55,
            r=20,
            b=70
        ),
        hoverlabel=dict(
            bgcolor='#FFA200',
        )
    )
