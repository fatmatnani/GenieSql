# Hacer los importes
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
from custom_sql_database import CustomSQLDatabase

# Import necessary LangChain libraries
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql.base import SQLDatabaseChain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


# manajando la base de datos
import sqlite3
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

# fxn make execution
def sql_executor(raw_code):
    c.execute(raw_code)
    data = c.fetchall()
    return data

city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']



def create_conversational_chain(db_path, gemini_api_key):
    # Get the instance of LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key, convert_system_message_to_human=True, temperature=0.0)
    # Get the DB connection
    db = CustomSQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    sql_prompt_template = """
    Only use the following tables:
    {table_info}
    Question: {input}

    Given an input question, first create a syntactically correct
    {dialect} query to run.
    
    Relevant pieces of previous conversation:
    {history}

    (You do not need to use these pieces of information if not relevant)
    Dont include ```, ```sql and \n in the output.
    """
    prompt = PromptTemplate(
            input_variables=["input", "table_info", "dialect", "history"],
            template=sql_prompt_template,
        )
    memory = ConversationBufferMemory(memory_key="history")

    db_chain = SQLDatabaseChain.from_llm(
            llm, db, memory=memory, prompt=prompt, return_direct=True,  verbose=True
        )

    output_parser = StrOutputParser()
    chain = llm | output_parser
    
    return db_chain, chain

def main():
    st.title("SQL Playground")
    st_lottie('https://lottie.host/6f4ee854-3625-4849-8985-e423a0752949/hZWZsrb0zk.json', key="user")
    menu = ["SQL Playground", "Genie SQL"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "SQL Playground":
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

        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # results
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    elif choice == "Genie SQL":
        st.subheader("Genie SQL")
        gemini_api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")

        if gemini_api_key:
            db_path = 'data/world.sqlite'
            db_chain, chain = create_conversational_chain(db_path, gemini_api_key)

            user_input = st.text_input("Ask a question in natural language:")
            if user_input:
                response = db_chain.run(user_input)
                st.write(f"Answer: {response}")

            # Display database information
            st.subheader("Database Information")

            # Display table information
            st.markdown("### Table Information")
            table_info = {'city': city, 'country': country, 'countrylanguage': countrylanguage}
            st.write(table_info)

            # Display table data using pandas
            st.markdown("### Table Data")
            tables = ['city', 'country', 'countrylanguage']
            for table in tables:
                st.subheader(f"{table.capitalize()} Table")
                query = f"SELECT * FROM {table}"
                data = sql_executor(query)
                df = pd.DataFrame(data, columns=[col.split(",")[0] for col in table_info[table]])
                st.dataframe(df)

if __name__ == '__main__':
    main()
