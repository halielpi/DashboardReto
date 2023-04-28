import pandas as pd 
import numpy as np 
import plotly.express as px 

sio_file_comisiones = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/comisiones.csv'
sio_file_emision = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/emision.csv'
sio_file_siniestros = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/siniestros.csv'
sio_file_ors_entidades = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/Ors_entidad.csv'


df_comisiones = pd.read_csv(sio_file_comisiones, encoding = 'cp1252', sep=',', on_bad_lines= 'warn'  )
df_emision = pd.read_csv(sio_file_emision, encoding = 'cp1252', sep=',', on_bad_lines= 'warn' )
df_siniestros= pd.read_csv(sio_file_siniestros, encoding = 'cp1252', sep=',', on_bad_lines= 'warn' )
ors_entidades_df= pd.read_csv(sio_file_ors_entidades)

df_emision = df_emision.dropna()
df_siniestros = df_siniestros.dropna()
df_siniestros = df_siniestros.dropna()
df_emision = df_emision[df_emision['ENTIDAD ']!='No disponible ']

def bar_emision():

    df_grouped = df_emision.groupby(['SEXO', 'ENTIDAD '])['SEXO'].count().reset_index(name='count')
    fig = px.bar(df_grouped, x='ENTIDAD ', y='count', color='SEXO', barmode='stack', height=600, width=900)
    fig.update_layout(xaxis_tickangle=-90, xaxis_title='Estado', yaxis_title='Número de personas', title='Número de personas por sexo en cada entidad')
    return fig

def plot_barras():
    barras = df_emision.groupby('ENTIDAD ')['SUMA ASEGURADA'].sum().reset_index()
    fig = px.bar(barras, x='ENTIDAD ', y='SUMA ASEGURADA', color='ENTIDAD ', height=500, width=1000)
    fig.update_layout(title='Suma Asegurada por Estado en MDP', xaxis_title="Estados", yaxis_title="Suma asegurada en Millones")
    fig.update_yaxes(tickformat=".2f", title='Suma asegurada en Millones')
    return fig

def plot_formas():
    formas = df_emision.groupby('FORMA DE VENTA')['FORMA DE VENTA'].count().reset_index(name='Suma')
    formas.sort_values(by='Suma', ascending=False, inplace=True)
    fig = px.bar(formas, x='FORMA DE VENTA', y='Suma', color='FORMA DE VENTA', height=500, width=1000)
    fig.update_layout(title='Formas de venta de seguros',
                      xaxis_title="Forma de venta",
                      yaxis_title="Cantidad de ventas",
                      xaxis_tickangle=-90)
    return fig
    
    