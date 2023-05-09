import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objs as go


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

columns = ['NUMERO DE ASEGURADOS', 'PRIMA CEDIDA', 'COMISIONES DIRECTAS', 'FONDO DE INVERSIîN', 'FONDO DE ADMINISTRACION', 'MONTO DE DIVIDENDOS', 'MONTO DE RESCATE']
for col in columns:
    df_comisiones[col] = pd.to_numeric(df_comisiones[col].replace('[^0-9\.-]','',regex=True), downcast='float')

columns = ['SUMA ASEGURADA', 'PRIMA EMITIDA', 'NUMERO DE ASEGURADOS', 'EDAD']

for col in columns:
    df_emision[col] = pd.to_numeric(df_emision[col].replace('[^0-9\.-]','',regex=True), downcast='float')

columns2 = ['MONTO RECLAMADO', 'MONTO PAGADO', 'NUMERO DE SINIESTROS', 'MONTO DE REASEGURO', ]

for col2 in columns2:
    df_siniestros[col2] = pd.to_numeric(df_siniestros[col2].replace('[^0-9\.-]','',regex=True), downcast='float')

def sexo_por_entidad():

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

def formas_ventas():
    formas = df_emision.groupby('FORMA DE VENTA')['FORMA DE VENTA'].count().reset_index(name='Suma')
    formas.sort_values(by='Suma', ascending=False, inplace=True)
    fig = px.bar(formas, x='FORMA DE VENTA', y='Suma', color='FORMA DE VENTA', height=500, width=1000)
    fig.update_layout(title='Formas de venta de seguros',
                      xaxis_title="Forma de venta",
                      yaxis_title="Cantidad de ventas",
                      xaxis_tickangle=-90)
    return fig
    

def piramide_poblacional():
    # Agrupar la población por edad y sexo
    df_poblacion = df_emision.groupby(['EDAD', 'SEXO']).size().reset_index(name='poblacion')

    # Crear un nuevo DataFrame con los resultados de la agrupación
    df_piramide = pd.concat([
        df_poblacion[df_poblacion['SEXO'] == 'Masculino'].sort_values(by='EDAD'),
        df_poblacion[df_poblacion['SEXO'] == 'Femenino'].sort_values(by='EDAD', ascending=False)
    ], ignore_index=True)

    # Crear la figura
    fig = go.Figure()

    # Agregar las barras de la población
    fig.add_trace(
        go.Bar(
            x=-df_piramide[df_piramide['SEXO'] == 'Femenino']['poblacion'],
            y=df_piramide[df_piramide['SEXO'] == 'Femenino']['EDAD'],
            orientation='h',
            name='Población Femenina',
            marker_color='#FFC0CB'
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_piramide[df_piramide['SEXO'] == 'Masculino']['poblacion'],
            y=df_piramide[df_piramide['SEXO'] == 'Masculino']['EDAD'],
            orientation='h',
            name='Población Masculina',
            marker_color='#ADD8E6'
        )
    )

    # Configurar el diseño del gráfico
    fig.update_layout(
        title='Pirámide poblacional por género y edad',
        xaxis=dict(title='Población'),
        yaxis=dict(title='Edad'),
        barmode='overlay',
        bargap=0.1,
        legend=dict(
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        )
    )

    # Mostrar el gráfico
    return fig

def cobertura():
    frecuencia_cobertura = df_emision['COBERTURA'].value_counts()

    # Crear el gráfico de barras
    fig = px.bar(frecuencia_cobertura, x=frecuencia_cobertura.index, y='COBERTURA', color='COBERTURA', height=500, width=1000)

    # Configurar el título y etiquetas del eje
    fig.update_layout(title='Frecuencia de la variable "COBERTURA"',
                    xaxis_title='Cobertura',
                    yaxis_title='Frecuencia')

    # Mostrar el gráfico
    return fig

def modalidad_poliza():
    modalidad = df_emision['MODALIDAD DE LA POLIZA'].value_counts().reset_index()

    fig = px.bar(modalidad, x='index', y='MODALIDAD DE LA POLIZA', color='index',
                title='Modalidad de la Póliza',
                labels={'index': 'Modalidad', 'MODALIDAD DE LA POLIZA': 'Frecuencia'}, height=500, width=1000)

    return fig

def siniestros():
    barras3= df_siniestros.groupby('CAUSA DEL SINIESTRO')['CAUSA DEL SINIESTRO'].count()
    barras3 = barras3.to_frame('Count')
    barras3.reset_index(inplace=True) 
    barras3.sort_values( by = 'Count', ascending = False, inplace = True )
    
    barras3 = pd.DataFrame({'CAUSA DEL SINIESTRO': barras3['CAUSA DEL SINIESTRO'].head(15), 'Count': barras3['Count'].head(15)})

    # Utilizamos la función pie de Plotly Express para generar un gráfico de pie
    fig = px.pie(barras3, values='Count', names='CAUSA DEL SINIESTRO', title='Mayores 15 causas de Siniestro',
                labels={'CAUSA DEL SINIESTRO':'Causa del siniestro', 'Count':'Porcentaje'}, height=500, width=1000)

    return fig

def siniestros_por_monto_pagado():
    barras4= df_siniestros.groupby('CAUSA DEL SINIESTRO')['MONTO PAGADO'].sum()
    barras4 = barras4.to_frame('Count')
    barras4.reset_index(inplace=True) 

    pie2 = pd.DataFrame({'CAUSA DEL SINIESTRO': barras4['CAUSA DEL SINIESTRO'].head(15), 'Count': barras4['Count'].head(15)})

    fig = px.pie(pie2, values='Count', names='CAUSA DEL SINIESTRO', title='Mayores 10 causas de Siniestro según el monto pagado',
                labels={'CAUSA DEL SINIESTRO':'Causa del siniestro', 'Count':'Porcentaje'}, height=500, width=1000)
    return fig