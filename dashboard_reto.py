import dash
from dash import dcc
from dash import html 
import plotly.graph_objects as go

import pandas as pd

from graph import *

app = dash.Dash()

app.layout = html.Div([
    html.H1('Dashboard para CNSF', style={'textAlign':'center','color':'#1a2e9c', 'background-color': 'lightblue'}),
    html.H3('Dashboard hecho por:'),
    html.Ul([
        html.Li('Alejandra Núñez Galindo (A01654136)'),
        html.Li('Diego Armando Cortés Mendoza (A01653915)'),
        html.Li('Haliel Pichardo Jaime (A01654497)'),
        html.Li('Jorge Jair Licea Ávalos (A01654956)'),
        html.Li('Maximiliano Barajas Chávez (A01654403)'),
        ]),
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