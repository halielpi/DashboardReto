import dash
from dash import dcc, html, Dash, dash_table
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import collections



from graph import *

df_ORS = ors_entidades_df[["FECHA DE CORTE", "ENTIDAD", "PRIMA EMITIDA", "COMISION DIRECTA", "SUMA ASEGURADA", "MONTO DE SINIESTRALIDAD"]]
df_ORS['FECHA DE CORTE'] = pd.to_datetime(df_ORS['FECHA DE CORTE'])
df_prom = df_ORS.groupby(["FECHA DE CORTE", "ENTIDAD"]).mean().reset_index()


app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='memory-output'),
    dcc.Dropdown(options=[{'label': entidad, 'value': entidad} for entidad in df_prom.ENTIDAD.unique()],
                 value=['Distrito Federal', 'Estado de México'],
                 id='memory-states',
                 multi=True),
    dcc.Dropdown(options=[{'label': 'PRIMA EMITIDA', 'value': 'PRIMA EMITIDA'},
                          {'label': 'COMISION DIRECTA', 'value': 'COMISION DIRECTA'},
                          {'label': 'SUMA ASEGURADA', 'value': 'SUMA ASEGURADA'},
                          {'label': 'MONTO DE SINIESTRALIDAD', 'value': 'MONTO DE SINIESTRALIDAD'}],
                 value='PRIMA EMITIDA',
                 id='memory-field'),
    html.Div([
        dcc.Graph(id='memory-graph'),
        dash_table.DataTable(
            id='memory-table',
            columns=[{'name': i, 'id': i} for i in df_prom.columns]
        ),
    ])
])


@app.callback(Output('memory-output', 'data'),
              Input('memory-states', 'value'))
def filter_states(states_selected):
    if not states_selected:
        # Return all the rows on initial load/no country selected.
        return df_prom.to_dict('records')

    filtered = df_prom.query('ENTIDAD in @states_selected')


    return filtered.to_dict('records')


@app.callback(Output('memory-table', 'data'),
              Input('memory-output', 'data'))
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate

    return data

@app.callback(Output('memory-graph', 'figure'),
              Input('memory-output', 'data'),
              Input('memory-field', 'value'))
def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate

    print(data)  # Imprimir los datos filtrados

    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in data:

        a = aggregation[row['ENTIDAD']]

        a['name'] = row['ENTIDAD']
        a['mode'] = 'lines+markers'

        a['x'].append(row[field])
        a['y'].append(row['FECHA DE CORTE'])

    return {
        'data': [x for x in aggregation.values()]
    }

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=10450)
