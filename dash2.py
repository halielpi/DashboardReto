import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

from graph import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout =dbc.Container([
        html.H1('Dashboard para CNSF', style={'textAlign':'center','color':'#1a2e9c', 'background-color': 'lightblue'}),
        html.H3('Dashboard hecho por:'),
        html.Ul([
            html.Li('Alejandra Núñez Galindo (A01654136)'),
            html.Li('Diego Armando Cortés Mendoza (A01653915)'),
            html.Li('Haliel Pichardo Jaime (A01654497)'),
            html.Li('Jorge Jair Licea Ávalos (A01654956)'),
            html.Li('Maximiliano Barajas Chávez (A01654403)'),
        ]),
        
        dbc.Alert('Hello, Bootstrap', className='m-5'),
  
        dbc.Tabs([
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Perfil de los asegurados'),
                            html.Hr(),
                            dcc.Graph(
                                id='graph_1',
                                figure=sexo_por_entidad(),
                                style={'width': '50%'}
                            ),
                            dcc.Graph(
                                id='graph_3',
                                figure=piramide_poblacional(),
                                style={'width': '50%'}
                            ),
                            dcc.Graph(
                                id='graph_4',
                                figure=plot_barras(),
                                style={'width': '50%'}
                            ),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Tab1'),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Características de las pólizas de seguro'),
                            html.Hr(),
                            dcc.Graph(
                                id='graph_2',
                                figure=formas_ventas(),
                                style={'width': '50%'}
                            ),
                             dcc.Graph(
                                id='graph_5',
                                figure=modalidad_poliza(),
                                style={'width': '50%'}
                            ),
                            dcc.Graph(
                                id='graph_6',
                                figure=cobertura(),
                                style={'width': '50%'}
                            ),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Tab2'),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Para qué se aseguran las personas?'),
                            html.Hr(),
                            dcc.Graph(
                                id='graph_7',
                                figure=siniestros(),
                                style={'width': '50%'}
                            ),
                            dcc.Graph(
                                id='graph_8',
                                figure=siniestros_por_monto_pagado(),
                                style={'width': '50%'}
                            ),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Tab3'),        
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)