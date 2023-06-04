import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output

from graph import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout =dbc.Container([
        html.Img(src='/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/IMG/Logo.png'),
        html.H3('Dashboard hecho por:', style={'color':'#13322B'}),
        html.Div(
            children=[
        html.Ul([
                    html.Li('Alejandra Núñez Galindo (A01654136)'),
                    html.Li('Diego Armando Cortés Mendoza (A01653915)'),
                    html.Li('Haliel Pichardo Jaime (A01654497)')
                ])
            ],
            style={'width': '50%', 'float': 'left'}
        ),
        html.Div(
            children=[
                html.Ul([
                    html.Li('Jorge Jair Licea Ávalos (A01654956)'),
                    html.Li('Maximiliano Barajas Chávez (A01654403)')
                ])
            ],
            style={'width': '50%', 'float': 'right'}
        ),
        dbc.Tabs([
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Perfil de los asegurados'),
                            html.Hr(),
                            
                            dbc.RadioItems(
                                id="radios",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Género", "value": 1},
                                    {"label": "Edad", "value": 2},
                                    {"label": "Suma Aseg", "value": 3},
                                ],
                                value=1,
                            ),
                        
                            html.Div(id="output"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Quién', 
                label_style={"color": "#A38C5B"} ,
                active_tab_style={"textTransform": "uppercase"},
                activeTabClassName="fw-bold"),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Características de las pólizas de seguro'),
                            html.Hr(),
                            
                            dbc.RadioItems(
                                id="radios-2",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Forma de venta", "value": 1},
                                    {"label": "Modalida de póliza", "value": 2},
                                    {"label": "Cobertura", "value": 3},
                                ],
                                value=1,
                            ),
                            html.Div(id="output-2"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Qué', 
                label_style={"color": "#A38C5B"},
                active_tab_style={"textTransform": "uppercase"},
                activeTabClassName="fw-bold"),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Para qué se aseguran las personas?'),
                            html.Hr(),
                            
                            dbc.RadioItems(
                                id="radios-3",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Siniestros 1", "value": 1},
                                    {"label": "Siniestros 2", "value": 2},
                                ],
                                value=1,
                            ),
                            html.Div(id="output-3"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Para qué', abel_style={"color": "#A38C5B"} ,active_tab_style={"textTransform": "uppercase"},
                activeTabClassName="fw-bold"),      
            ])
])

@app.callback(Output("output", "children"), [Input("radios", "value")])
def display_value_1(value):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = sexo_por_entidad()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = piramide_poblacional()
    elif value == 3:
        # Crear la gráfica para la opción 3
        fig = plot_barras()
    return dcc.Graph(figure=fig)

@app.callback(Output("output", "children"), [Input("radios", "value")])
def display_value_1(value):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = sexo_por_entidad()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = piramide_poblacional()
    elif value == 3:
        # Crear la gráfica para la opción 3
        fig = plot_barras()
    return dcc.Graph(figure=fig)

@app.callback(Output("output-2", "children"), [Input("radios-2", "value")])
def display_value_2(value):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = formas_ventas()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = modalidad_poliza()
    elif value == 3:
        # Crear la gráfica para la opción 2
        fig = cobertura()
    return dcc.Graph(figure=fig)

@app.callback(Output("output-3", "children"), [Input("radios-3", "value")])
def display_value_3(value):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = siniestros()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = siniestros_por_monto_pagado()
    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)