import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objs as go
import requests


sio_file_comisiones = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/comisiones.csv'
sio_file_emision = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/emision.csv'
sio_file_siniestros = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/siniestros.csv'
sio_file_ors_entidades = '/Users/xariselpichardojaime/Desktop/My Python/DashboardReto/downloads/Ors_entidad.csv'


df_comisiones = pd.read_csv(sio_file_comisiones, encoding = 'utf-8', sep=',', on_bad_lines= 'warn'  )
df_emision = pd.read_csv(sio_file_emision, encoding = 'utf-8', sep=',', on_bad_lines= 'warn' )
df_siniestros= pd.read_csv(sio_file_siniestros, encoding = 'utf-8', sep=',', on_bad_lines= 'warn' )
ors_entidades_df= pd.read_csv(sio_file_ors_entidades)

df_emision = df_emision.dropna()
df_siniestros = df_siniestros.dropna()
df_siniestros = df_siniestros.dropna()
df_emision = df_emision[df_emision['ENTIDAD ']!='No disponible ']

columns = ['NUMERO DE ASEGURADOS', 'PRIMA CEDIDA', 'COMISIONES DIRECTAS', 'FONDO DE INVERSIÓN', 'FONDO DE ADMINISTRACION', 'MONTO DE DIVIDENDOS', 'MONTO DE RESCATE']
for col in columns:
    df_comisiones[col] = pd.to_numeric(df_comisiones[col].replace('[^0-9\.-]','',regex=True), downcast='float')

columns = ['SUMA ASEGURADA', 'PRIMA EMITIDA', 'NUMERO DE ASEGURADOS', 'EDAD']

for col in columns:
    df_emision[col] = pd.to_numeric(df_emision[col].replace('[^0-9\.-]','',regex=True), downcast='float')

columns2 = ['MONTO RECLAMADO', 'MONTO PAGADO', 'NUMERO DE SINIESTROS', 'MONTO DE REASEGURO', ]

for col2 in columns2:
    df_siniestros[col2] = pd.to_numeric(df_siniestros[col2].replace('[^0-9\.-]','',regex=True), downcast='float')

ors_entidades_df= ors_entidades_df.apply(pd.to_numeric, downcast= "integer", errors= "ignore")
ors_entidades_df["AÑO"]= ors_entidades_df["AÑO"].apply(str)
ors_entidades_df["ENTIDAD"] = ors_entidades_df["ENTIDAD"].replace("Distrito Federal", "Ciudad de México")
ors_entidades_df["ENTIDAD"] = ors_entidades_df["ENTIDAD"].replace("Estado de México", "México")

ors_entidades_df.dropna(inplace=True)
columnas = ors_entidades_df.columns[5:-1]
ors_entidades_df[columnas] = ors_entidades_df[columnas].apply(lambda column: column.replace('[^0-9\'.-]','',regex=True))
ors_entidades_df = ors_entidades_df.apply(pd.to_numeric, downcast = "integer", errors="ignore") 

def sexo_por_entidad():

    df_grouped = df_emision.groupby(['SEXO', 'ENTIDAD '])['SEXO'].count().reset_index(name='count')
    fig = px.bar(df_grouped, x='ENTIDAD ', y='count', color='SEXO', barmode='stack', height=600, width=900)
    fig.update_layout(xaxis_tickangle=-90, xaxis_title='Estado', yaxis_title='Número de personas', title='Número de personas por sexo en cada entidad')
    return fig

def plot_barras(selected_years):
    if selected_years is not None:
        df_filtered = ors_entidades_df[ors_entidades_df['AÑO'].isin(selected_years)]
    else:
        df_filtered = ors_entidades_df
        
    # Resto del código existente
    barras = df_filtered.groupby('ENTIDAD')['SUMA ASEGURADA'].sum().reset_index()
    barras['SUMA ASEGURADA'] = barras['SUMA ASEGURADA']/1000000000
    barras.sort_values(by='SUMA ASEGURADA', ascending=False, inplace=True)

    fig = px.bar(barras, x='ENTIDAD', y='SUMA ASEGURADA',
                color_discrete_sequence=['#1E5C4E'],  
                height=600, width=1000,
               )

    fig.update_layout(title='Suma Asegurada por Estado en MDP',
                    xaxis_title="Estados",
                    yaxis_title="Suma asegurada en Millones")

    fig.update_yaxes(tickformat=".2f", title='Suma asegurada en Mil millones')

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
            marker_color='#bd609b'
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_piramide[df_piramide['SEXO'] == 'Masculino']['poblacion'],
            y=df_piramide[df_piramide['SEXO'] == 'Masculino']['EDAD'],
            orientation='h',
            name='Población Masculina',
            marker_color='#65b0c9'
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

def formas_ventas(selected_state):
    if selected_state is not None:
        formas = df_emision[df_emision['ENTIDAD '] == selected_state]
    else:
        formas = df_emision

    formas = formas.groupby('FORMA DE VENTA')['FORMA DE VENTA'].count().reset_index(name='Suma')
    formas.sort_values(by='Suma', ascending=False, inplace=True)
    fig = px.bar(formas, x='FORMA DE VENTA', y='Suma', color_discrete_sequence=['#1E5C4E'], height=600, width=1000)
    fig.update_layout(title='Formas de venta de seguros',
                      xaxis_title="Forma de venta",
                      yaxis_title="Cantidad de ventas",
                      xaxis_tickangle=-90)
    return fig

# Las otras dos funciones (modalidad_poliza y cobertura) deben seguir un enfoque similar

    

def cobertura(selected_state):
    if selected_state is not None:
        coberturas = df_emision[df_emision['ENTIDAD '] == selected_state]['COBERTURA']
    else:
        coberturas = df_emision['COBERTURA']

    frecuencia_cobertura = coberturas.value_counts()

    # Crear el gráfico de barras
    fig = px.bar(frecuencia_cobertura, x=frecuencia_cobertura.index, y='COBERTURA',
                 color_discrete_sequence=['#1E5C4E'],
                 height=600, width=1000)

    # Configurar el título y etiquetas del eje
    fig.update_layout(title='Frecuencia de la variable "COBERTURA"',
                      xaxis_title='Cobertura',
                      yaxis_title='Frecuencia')

    # Mostrar el gráfico
    return fig

def modalidad_poliza(selected_state):
    if selected_state is not None:
        modalidades = df_emision[df_emision['ENTIDAD '] == selected_state]['MODALIDAD DE LA POLIZA']
    else:
        modalidades = df_emision['MODALIDAD DE LA POLIZA']

    modalidad = modalidades.value_counts().reset_index()

    fig = px.bar(modalidad, x='index', y='MODALIDAD DE LA POLIZA',
                 color_discrete_sequence=['#1E5C4E'],  # Especificar un color verde para las barras
                 title='Modalidad de la Póliza',
                 labels={'index': 'Modalidad', 'MODALIDAD DE LA POLIZA': 'Frecuencia'},
                 height=500, width=1000)

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

def siniestros_bar(n):
    barras3 = df_siniestros.groupby('CAUSA DEL SINIESTRO')['CAUSA DEL SINIESTRO'].count()
    barras3 = barras3.to_frame('Count')
    barras3.reset_index(inplace=True)
    barras3.sort_values(by='Count', ascending=False, inplace=True)

    barras3 = pd.DataFrame({'CAUSA DEL SINIESTRO': barras3['CAUSA DEL SINIESTRO'].head(n), 'Count': barras3['Count'].head(n)})

    # Sort the DataFrame in descending order
    barras3.sort_values(by='Count', ascending=False, inplace=True)

    # Utilize the bar function of Plotly Express to create a horizontal bar chart
    fig = px.bar(barras3, x='Count', y='CAUSA DEL SINIESTRO', orientation='h',
                 title='Top {} causas de Siniestro'.format(n),
                 labels={'CAUSA DEL SINIESTRO': 'Causa del siniestro', 'Count': 'Cantidad'},
                 height=700, width=1000,
                 color_discrete_sequence=['#1E5C4E'])  # Establecer el color deseado (en este caso, azul)

    return fig

def siniestros_por_monto_pagado():
    barras4= df_siniestros.groupby('CAUSA DEL SINIESTRO')['MONTO PAGADO'].sum()
    barras4 = barras4.to_frame('Count')
    barras4.reset_index(inplace=True) 

    pie2 = pd.DataFrame({'CAUSA DEL SINIESTRO': barras4['CAUSA DEL SINIESTRO'].head(15), 'Count': barras4['Count'].head(15)})

    fig = px.pie(pie2, values='Count', names='CAUSA DEL SINIESTRO', title='Mayores 15 causas de Siniestro según el monto pagado',
                labels={'CAUSA DEL SINIESTRO':'Causa del siniestro', 'Count':'Porcentaje'}, height=500, width=1000)
    return fig

def mapa_mexico():
    repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json' 
    #Archivo GeoJSON
    mx_regions_geo = requests.get(repo_url).json()

    # Contar la frecuencia de cada estado
    estado_frecuencia = ors_entidades_df['ENTIDAD'].value_counts().reset_index()

    estado_frecuencia.columns = ['ENTIDAD', 'FRECUENCIA']
    estado_frecuencia['ENTIDAD'].str.capitalize()
    # print(estado_frecuencia)
    # Cargar los datos del mapa de México
    mexico = px.data.gapminder().query("country == 'Mexico'")
    data = estado_frecuencia[estado_frecuencia['ENTIDAD'] != 'Extranjero']



    df = pd.DataFrame({'estado':data['ENTIDAD'], 'frecuencia':data['FRECUENCIA']})


    fig = px.choropleth(data_frame=df, 
                        geojson=mx_regions_geo, 
                        locations=df['estado'], # nombre de la columna del Dataframe
                        featureidkey='properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                        color=df['frecuencia'], #El color depende de las cantidades
                        color_continuous_scale="greens",
                        height=800,  # Ajustar el alto del gráfico a 600 píxeles
                        width=1000,
                        title="Frecuencia de personas aseguradas por estado",
                        #scope="north america"
                    )

    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    return fig