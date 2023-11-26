import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Centros de Distribución") 
st.header('Centros de Distribución en base a los Centros de Vacunacaión en el Perú del 2020-21') 

df = pd.read_csv('centrovacunacion5.csv')

df_personas= df[['nombre', 'entidad_administra']].drop_duplicates().reset_index(drop=True)

df_personas2 = df_personas 

st.dataframe(df) #de esta forma nos va a mostrar el dataframe en Streamlit
st.subheader('Tabla de Entidades Administrativas') 
st.write(df_personas2) #este nos sirve cuando no tenemos dataframe sino objeto

st.subheader('Tabla de Entidades Administrativas por Cantidad') 
df_personas3= df["entidad_administra"].value_counts()
st.write(df_personas3)


#Crear un grafico de torta (pie chart)

pie_chart = px.pie(df_personas3, 
                   title = 'Entidades administrativas totales', 
                   values = df_personas3.values,
                   names = df_personas3.index) 

st.plotly_chart(pie_chart)


st.subheader('Filtrar Entidades y Centros de Vacunación por Latitud y Longitud') 
#Crear una lista con los parametros de una columna

entidades = df['entidad_administra'].unique().tolist() 
nombre = df['nombre'].unique().tolist() 
latitud = df['latitud'].unique().tolist() 
longitud= df['longitud'].unique().tolist() 

#Crear un slider 
latitud_selector = st.slider('Según la latitud:',
                          min_value = min(latitud), #el valor minimo va a ser el valor mas pequeño que encuentre dentro de la columna 
                          max_value = max(latitud),#el valor maximo va a ser el valor mas grande que encuentre dentro de la columna 
                          value = (min(latitud),max(latitud))) #que tome desde el minimo, hasta el maximo

longitud_selector = st.slider('Según la longitud:',
                          min_value = min(longitud), #el valor minimo va a ser el valor mas pequeño que encuentre dentro de la columna 
                          max_value = max(longitud),#el valor maximo va a ser el valor mas grande que encuentre dentro de la columna 
                          value = (min(longitud),max(longitud))) #que tome desde el minimo, hasta el maximo


#crear multiselectores
entidad_selector = st.multiselect('Entidades:',
                                 entidades,
                                   default = [])
  
nombre_selector = st.multiselect('Nombre:',
                                          nombre,
                                         default = [])


filtros = (df['latitud'].between(*latitud_selector))or(df['longitud'].between(*longitud_selector))or(df['entidad_administra'].isin(entidad_selector))or(df['nombre'].isin(nombre_selector))

numero_resultados = df[filtros].shape[0]
st.subheader('Filtered Results')
st.write(df[filtros])
st.markdown(f'*Resultados Disponibles:{numero_resultados}*') 
