import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
from dash import dcc, html, Dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output
from dash.dependencies import Input, Output


from graph2 import *

# Crear la aplicación de Dash

# Crear la aplicación de Dash
app = dash.Dash(__name__)

df_ORS = ors_entidades_df[["FECHA DE CORTE", "RAMO", "ENTIDAD", "PRIMA EMITIDA", "COMISION DIRECTA", "SUMA ASEGURADA", "MONTO DE SINIESTRALIDAD"]]
df_ORS_prima = df_ORS[["FECHA DE CORTE", "RAMO", "ENTIDAD", "PRIMA EMITIDA"]]

    # Quitar negativos
df_ORS_prima = df_ORS_prima[(df_ORS_prima[["PRIMA EMITIDA"]] > 0).all(1)]
df_ORS_prima['FECHA DE CORTE'] = pd.to_datetime(df_ORS_prima['FECHA DE CORTE'])

    # Obtener las listas de estados y ramos únicos
estados = df_ORS_prima['ENTIDAD'].unique()
ramos = df_ORS_prima['RAMO'].unique()

# Función para generar la gráfica
def generar_grafica_promedio_prima(filtered_data):
    promedios_por_fecha = filtered_data.groupby("FECHA DE CORTE")["PRIMA EMITIDA"].mean()

    fig = px.line(promedios_por_fecha, x=promedios_por_fecha.index, y=promedios_por_fecha.values,
                  title="Promedio de Prima Emitida por Fecha de Corte",
                  labels={"x": "Fecha de corte", "y": "Promedio por fecha"},
                  markers=True)

    return fig

# Definir el layout de la aplicación
app.layout = html.Div([
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

# Definir la función de callback para actualizar la gráfica
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

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
