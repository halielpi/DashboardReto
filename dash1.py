import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output
from dash.dependencies import Input, Output


from graph2 import *

image_path = 'assets/Logo2.png' 

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout =dbc.Container([
        html.Img(src=image_path),
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
                                value=None,
                                placeholder="Selecciona una estado"
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
                                    {"label": "Prima", "value": 4},
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
                                id="dropdown-5",
                                options=[
                                    {'label': estado, 'value': estado} for estado in df_siniestros['ENTIDAD'].unique()
                                ],
                                value=None,
                                placeholder="Selecciona una estado"
                            ),

                            dbc.RadioItems(
                                id="radios-3",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-custom",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Siniestros", "value": 1},
                                    {"label": "Siniestros segun MP", "value": 2},
                                    {"label": "Piramide siniestros", "value": 3},
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


@app.callback(Output("output", "children"), [Input("radios", "value")])
def update_graph_1(value):
    if value == 4:
        return html.Div([
                dcc.Dropdown(
                    id="dropdown-4",
                    options=[
                        {'label': str(year), 'value': year} for year in ors_entidades_df['AÑO'].unique()
                    ],
                    value=None,
                    multi=True,
                    style={'color': '#A38C5B'},
                    placeholder="Selecciona una año"
                ),
                html.Div(id="output-4")  # Aquí se mostrará la gráfica actualizada
            ])

    elif value == 1:
        fig = mapa_mexico()
    elif value == 2:
        fig = sexo_por_entidad()
    elif value == 3:
        fig = piramide_poblacional()
    return dcc.Graph(figure=fig)

@app.callback(Output("output-4", "children"), [Input("dropdown-4", "value")])
def update_graph_4(selected_years):
    # Actualiza la gráfica según los años seleccionados
    fig = plot_barras(selected_years)
    # Devuelve la gráfica actualizada dentro del dcc.Graph
    return dcc.Graph(figure=fig)


@app.callback(Output("output-2", "children"), [Input("radios-2", "value"), Input("dropdown-2", "value")])
def update_graph_2(value, selected_state):
    if value == 1:
        fig = formas_ventas(selected_state)
    elif value == 2:
        fig = modalidad_poliza(selected_state)
    elif value == 3:
        fig = cobertura(selected_state)
    elif value == 4:
        return html.Div([
            html.H1("Gráfica de Promedio de Prima Emitida por Fecha de Corte"),
            dcc.Dropdown(
                id="dropdown-estado",
                options=[{'label': estado, 'value': estado} for estado in estados],
                value=None,
                placeholder="Selecciona un estado"
            ),
            dcc.Dropdown(
                id="dropdown-ramo",
                options=[{'label': ramo, 'value': ramo} for ramo in ramos],
                value=None,
                placeholder="Selecciona un ramo"
            ),
            dcc.Graph(id="line-chart")
        ])
    return dcc.Graph(figure=fig)


@app.callback(Output("output-3", "children"), [Input("radios-3", "value"), Input("dropdown-5", "value")])
def display_value_3(value, selected_state):
    if value == 1:
        fig = siniestros(selected_state)
    elif value == 2:
        fig = siniestros_por_monto_pagado(selected_state)
    elif value ==3:
        return html.Div([
                    dcc.Dropdown(
                        id="dropdown-causa",
                        options=[
                            {'label': causa, 'value': causa} for causa in df_siniestros['CAUSA DEL SINIESTRO'].unique()
                        ],
                        value=None,
                        multi=False,
                        placeholder="Selecciona una causa de siniestro"
                    ),
                    dcc.Graph(id="grafica-piramide")
                ])

    return dcc.Graph(figure=fig)

@app.callback(Output("grafica-piramide", "figure"),Input("dropdown-causa", "value"))
def actualizar_piramide(causa_siniestro):
    return piramide_siniestros(causa_siniestro)

@app.callback(
    Output("line-chart", "figure"),
    [Input("dropdown-estado", "value"), Input("dropdown-ramo", "value")]
)
def update_line_chart(selected_state, selected_ramo):
    filtered_data = df_ORS_prima

    if selected_state:
        filtered_data = filtered_data[filtered_data['ENTIDAD'] == selected_state]
    if selected_ramo:
        filtered_data = filtered_data[filtered_data['RAMO'] == selected_ramo]

    fig = generar_grafica_promedio_prima(filtered_data)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)