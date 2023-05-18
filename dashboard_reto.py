import dash
from dash import dcc, dash_table, dcc, callback, Output, Input
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
    dcc.RadioItems(options=['Género', 'Suma asegurada', ], value='Género', id='controls-and-radio-item'),
    dash_table.DataTable(data=df_emision.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph'),

])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df_emision, x='ENTIDAD ', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)