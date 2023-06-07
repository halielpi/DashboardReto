import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output
from dash.dependencies import Input, Output


from graph2 import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout =dbc.Container([
        html.H1('Dashboard para CNSF', style={'textAlign':'center','color':'white', 'background-color': '#1E5C4E'}),
        html.Img(src='./IMG/Logo.png'),
        html.H3('Dashboard hecho por:', style={'color':'#13322B'}),
        dbc.Row([
        dbc.Col([
            html.Ul([
                html.Li('Alejandra Núñez Galindo (A01654136)'),
                html.Li('Diego Armando Cortés Mendoza (A01653915)'),
                html.Li('Haliel Pichardo Jaime (A01654497)')
            ]),
        ], width=6),

        dbc.Col([
            html.Ul([
                html.Li('Jorge Jair Licea Ávalos (A01654956)'),
                html.Li('Maximiliano Barajas Chávez (A01654403)')
            ]),
        ], width=6),
    ], className='mb-4'),
        
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
                                labelClassName="btn btn-custom",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Entidad", "value": 1},
                                    {"label": "Género", "value": 2},
                                    {"label": "Edad", "value": 3},
                                    {"label": "Suma Aseg", "value": 4},
                                ],
                                value=1,
                                style={"color": "#1E5C4E", "border-color": "#1E5C4E"},
                            ),
                            
                            dcc.Dropdown(
                                id="dropdown-1",
                                options=[
                                    {'label': str(year), 'value': year} for year in ors_entidades_df['AÑO'].unique()
                                ],
                                value=None,
                                multi=True
                            ),
                            
                            html.Div(id="output"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Quién',active_tab_style={"textTransform": "uppercase"}, label_style={"color": "#A38C5B"},
                activeTabClassName="fw-bold"),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Características de las pólizas de seguro'),
                            html.Hr(),
                            dcc.Dropdown(
                                id="dropdown-2",
                                options=[
                                    {'label': estado, 'value': estado} for estado in df_emision['ENTIDAD '].unique()
                                ],
                                value=None
                            ),

                            dbc.RadioItems(
                                id="radios-2",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-custom",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Forma de venta", "value": 1},
                                    {"label": "Modalida de póliza", "value": 2},
                                    {"label": "Cobertura", "value": 3},
                                ],
                                value=1,
                                style={"color": "#1E5C4E", "border-color": "#1E5C4E"},
                            ),
                            html.Div(id="output-2"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Qué',active_tab_style={"textTransform": "uppercase"},label_style={"color": "#A38C5B"},
                activeTabClassName="fw-bold"),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Para qué se aseguran las personas?'),
                            html.Hr(),
                            
                            dcc.Dropdown(
                                    options=[
                                        {'label': 'Option 1', 'value': 1},
                                        {'label': 'Option 2', 'value': 2},
                                        {'label': 'Option 3', 'value': 3}
                                    ],
                                    value=None
                                ),
                            dbc.RadioItems(
                                id="radios-3",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-custom",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Siniestros 1", "value": 1},
                                    {"label": "Siniestros 2", "value": 2},
                                    {"label": "Siniestros 3", "value": 3},
                                ],
                                value=1,
                                style={"color": "#1E5C4E", "border-color": "#1E5C4E"},
                            ),
                            html.Div(id="output-3"),
                        ]  
                    ),
                    className='mt-3'                
                ),
                label='Para qué',active_tab_style={"textTransform": "uppercase"},label_style={"color": "#A38C5B"},
                activeTabClassName="fw-bold"),      
            ])
])


@app.callback(Output("output", "children"), [Input("radios", "value"), Input("dropdown-1", "value")])
def update_graph_1(value, selected_years):
    if value == 4:
        return html.Div([
            dcc.Dropdown(
                id="dropdown-1",
                options=[
                    {'label': str(year), 'value': year} for year in ors_entidades_df['AÑO'].unique()
                ],
                value=None,
                multi=True
            ),
            dcc.Graph(figure=plot_barras(selected_years))
        ])
    elif value == 1:
        # Crear la gráfica para la opción 1
        fig = mapa_mexico()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = sexo_por_entidad()
    elif value == 3:
        # Crear la gráfica para la opción 3
        fig = piramide_poblacional()
    return dcc.Graph(figure=fig)

@app.callback(Output("output-2", "children"), [Input("radios-2", "value"), Input("dropdown-2", "value")])
def update_graph_2(value, selected_state):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = formas_ventas(selected_state)
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = modalidad_poliza(selected_state)
    elif value == 3:
        # Crear la gráfica para la opción 3
        fig = cobertura(selected_state)
    return dcc.Graph(figure=fig)

@app.callback(Output("output-3", "children"), [Input("radios-3", "value")])
def display_value_3(value):
    if value == 1:
        # Crear la gráfica para la opción 1
        fig = siniestros()
    elif value == 2:
        # Crear la gráfica para la opción 2
        fig = siniestros_por_monto_pagado()
    elif value == 3:
        return html.Div([
            html.H1('Top Causas de Siniestro', style={'textAlign': 'center', 'color':'#13322B'}),
            html.Label('Selecciona el número de causas a mostrar:'),
            dcc.Input(id='input-top-n', type='number', value=10, min=1, max=20, step=1),
            dcc.Graph(id='bar-chart')
        ])

    return dcc.Graph(figure=fig)

@app.callback(Output('bar-chart', 'figure'), [Input('input-top-n', 'value')])
def update_bar_chart(n):
    fig = siniestros_bar(n)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)