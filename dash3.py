import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

from graph import *

carousel=dbc.Carousel(
    items=[
        {"key": "1", "children": dcc.Graph(
                                    id='graph_4',
                                    figure=plot_barras(),
                                    style={'width': '50%'}
            )
        },
        {"key": "2", "children":dcc.Graph(
                                    id='graph_3',
                                    figure=piramide_poblacional(),
                                    style={'width': '50%'}
                                    )
        },
        {"key": "3", "children": dcc.Graph(
                                    id='graph_1',
                                    figure=sexo_por_entidad(),
                                    style={'width': '50%'}
                                    )
        }
    ],
    controls=True,
    indicators=True,
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Agregar el carrusel a la aplicación Dash
app.layout = dbc.Container(carousel, className="mt-4")

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)