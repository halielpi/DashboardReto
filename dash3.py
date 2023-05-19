import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

from graph import *
from dash import Input, Output, html

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.RadioItems(
            id="radios-1",
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

        dbc.RadioItems(
            id="radios-2",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Forma de venta", "value": 4},
                {"label": "Modalida de póliza", "value": 5},
                {"label": "Cobertura", "value": 6},
            ],
            value=1,
        ),
         html.Div(id="output"),

        dbc.RadioItems(
            id="radios-3",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Siniestros 1", "value": 7},
                {"label": "Siniestros 2", "value": 8},
            ],
            value=1,
        ),
        html.Div(id="output"),
    ],
    className="radio-group",
)

@app.callback(Output("output", "children"), [Input("radios-1", "value"), Input("radios-2", "value"), Input("radios-3", "value")])
def display_value(value1, value2, value3):
    if value1 == 1:
        # Crear la gráfica para la opción 1
        fig = sexo_por_entidad()
    elif value1 == 2:
        # Crear la gráfica para la opción 2
        fig = piramide_poblacional()
    elif value1 == 3:
        # Crear la gráfica para la opción 3
        fig = plot_barras()
    elif value2 == 4:
        # Crear la gráfica para la opción 4
        fig = formas_ventas()
    elif value2 == 5:
        # Crear la gráfica para la opción 5
        fig = modalidad_poliza()
    elif value2 == 6:
        # Crear la gráfica para la opción 6
        fig = cobertura()
    elif value3 == 7:
        # Crear la gráfica para la opción 7
        fig = siniestros()
    elif value3 == 8:
        # Crear la gráfica para la opción 8
        fig = siniestros_por_monto_pagado()
    else:
        # Opción por defecto si el valor no coincide con ninguna opción
        fig = go.Figure()

    # Devolver la gráfica como salida
    return dcc.Graph(figure=fig)


# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
    
    