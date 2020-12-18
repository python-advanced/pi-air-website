import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from db_wrapper import DbWrapper
from get_graphs import get_graphs
from utils import get_account_text


external_stylesheets = ["https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
                        "https://cdn.rawgit.com/yclliu/dash-css/37c322c/main.css"]

db_wrapper = DbWrapper()

app = dash.Dash('Live Air Quality', external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Pi-Air'

content = [
    html.Div([
        html.Div(id='accounts-status-text', className=''),
    ], className='row accounts-status'),

    html.Div(children=html.Div(id='main-graphs'), className='row'),
    dcc.Interval(id='interval-component-main', interval=30 * 1000, n_intervals=0),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(id='interval-component', interval=3 * 1000, n_intervals=0),

    html.Footer(html.Div(html.Div(
        html.Div(html.Span('Python-Advanced Course Pi-Air Project'), className='col-sm-8 col-sm-offset-2 text-center'),
        className='row'), className='container'), className='footer-padding')
]

app.layout = html.Div([
    html.Div([html.H2('Pi-Air')], className='navbar navbar-default navbar-fixed-top'),
    html.Div(content, className="container")
])


@app.callback(Output('accounts-status-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_accounts_status(n_intervals):
    class_choice = 'col-xs-12 col-sm-6 col-md-6 col-lg-6'
    sensor_online = db_wrapper.is_online()
    status_text_1, status_class_name_1 = get_account_text(sensor_online)

    return html.Div([
        html.Span('在線狀態： Sensor: '),
        html.Span(status_text_1),
        html.Span('', className=status_class_name_1)
    ], className=class_choice)


@app.callback(
    Output('main-graphs', 'children'),
    [Input('interval-component-main', 'n_intervals')])
def update_main_graphs(n_intervals):
    return get_graphs(db_wrapper, is_main_graphs=True)


@app.callback(
    Output('graphs', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_graphs(n_intervals):
    return get_graphs(db_wrapper, is_main_graphs=False)


if __name__ == '__main__':
    app.run_server(debug=True)
