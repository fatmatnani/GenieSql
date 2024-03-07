# Hacer los importes
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd

# manajando la base de datos
import sqlite3
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

#fxn make execution
def sql_executor(raw_code):
    c.execute(raw_code)
    data = c.fetchall()
    return data

city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']


def main():
    st.title("SQL Playground")
    st_lottie('https://lottie.host/6f4ee854-3625-4849-8985-e423a0752949/hZWZsrb0zk.json', key="user")
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Homepage")
        # Columnas de la pagina
        col1,col2 = st.columns(2)
        with col1:
            with st.form(key='query form'):
                raw_code = st.text_area("SQL CODE Here")
                submit_code = st.form_submit_button("Execute")
                # Tabla de info
                with st.expander("Table Info"):
                    table_info = {'city':city,'country':country,'countrylanguage':countrylanguage}
                    st.json(table_info)
				    
                    
                # resulta
                with col2:
                    if submit_code:
                        st.info("Query Submitted")
                        st.code(raw_code)

                        # results
                        query_results = sql_executor(raw_code)
                        with st.expander("Results)"):
                            st.write(query_results)

                        with st.expander("Pretty Table"):
                            query_df = pd.DataFrame(query_results)
                            st.dataframe(query_df)    

    else:
        st.subheader("Speak with your DB")


if __name__== '__main__':
    main()            