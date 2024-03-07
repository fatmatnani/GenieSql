# Importaciones necesarias para la aplicación
import streamlit as st  # Para animaciones
from streamlit_lottie import st_lottie
import pandas as pd  # Para manejar datos

# Configuración de la base de datos SQLite
import sqlite3
conn = sqlite3.connect('data/world.sqlite')   # Conexión a la base de datos
c = conn.cursor()   # Crear un cursor para ejecutar consultas

# Función para ejecutar código SQL raw y devolver los resultados
def sql_executor(raw_code):
    c.execute(raw_code)  # Ejecuta el código SQL
    data = c.fetchall()  # Recoge los resultados
    return data   # Devuelve los resultados

# Listas que contienen los campos de las tablas disponibles para consultas
city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']


def main():
    st.title("SQL Playground")  # Título de la aplicación
    st_lottie('https://lottie.host/6f4ee854-3625-4849-8985-e423a0752949/hZWZsrb0zk.json', key="user")   # Carga una animación de Lottie
    menu = ["Home", "About"]  # Menú lateral para navegar
    choice = st.sidebar.selectbox("Menu", menu)   # Selector del menú

    if choice == "Home":   # Si se elige Home
        st.subheader("Homepage")
        # Columnas de la pagina
        col1,col2 = st.columns(2)  # Divide la pantalla en dos columnas
        with col1:  # Primera columna
            with st.form(key='query form'):   # Formulario para la entrada de la consulta SQL
                raw_code = st.text_area("SQL CODE Here")  # Área de texto para ingresar el código SQL
                submit_code = st.form_submit_button("Execute")  # Botón para ejecutar la consulta
                # # Expansor para mostrar información de las tablas
                with st.expander("Table Info"):
                    table_info = {'city':city,'country':country,'countrylanguage':countrylanguage}
                    st.json(table_info) # Muestra la información de las tablas en formato JSON
				    
                    
                # # Segunda columna
                with col2: 
                    if submit_code:  # Si se ha enviado el código
                        st.info("Query Submitted")
                        st.code(raw_code)   # Muestra el código SQL enviado

                        # results
                        query_results = sql_executor(raw_code)  # Ejecuta la consulta y obtiene los resultados
                        with st.expander("Results)"):   # Expansor para mostrar los resultados crudos
                            st.write(query_results)

                        with st.expander("Pretty Table"): # Expansor para mostrar los resultados en una tabla bonita
                            query_df = pd.DataFrame(query_results)  # Convierte los resultados en un DataFrame de Pandas
                            st.dataframe(query_df)  # Muestra el DataFrame  

    else:  # Si se elige About
        st.subheader("Speak with your DB")  # Subtítulo de la sección About


if __name__== '__main__':
    main()            # Ejecuta la función principal
