import dash
from dash import dcc
from dash import html 
import plotly.graph_objects as go

import pandas as pd

from graph import *

app = dash.Dash()

app.layout = html.Div([
    html.H1('Dashboard para CNSF', style={'textAlign':'center','color':'#1a2e9c', 'background-color': 'lightblue'}),
    
    dcc.Graph(
        id='graph_1',
        figure=bar_emision(),
        style={'width': '50%'}
    ),
    dcc.Graph(
        id='graph_2',
        figure=plot_formas(),
        style={'width': '50%'}
    ),
    dcc.Graph(
        id='graph_3',
        figure=plot_barras(),
        style={'width': '50%'}
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)