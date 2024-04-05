import psycopg2
import streamlit as st
from utils import load_config

config = load_config()

def get_db_connection():
    return st.session_state.db_conn

def get_db_cursor(db_connection):
    return db_connection.cursor()

def get_db_connection_and_cursor():
    conn = get_db_connection()
    return conn, conn.cursor()

def close_db_connection():
    if 'db_conn' in st.session_state and st.session_state.db_conn is not None:
        st.session_state.db_conn.close()
        st.session_state.db_conn = None

def save_extracted_text(pdf_filename, extracted_text):
    conn, cursor = get_db_connection_and_cursor()

    cursor.execute('SELECT COUNT(id) FROM pdf_content;')
    total_pdf_content = cursor.fetchone()[0]
    id = int(total_pdf_content) + 1
    
    cursor.execute("INSERT INTO pdf_content (id, pdf_filename, extracted_text) VALUES (%s, %s, %s)", (id, pdf_filename, extracted_text))

    conn.commit()

def init_db():
    conn = psycopg2.connect(
        database=config["db"]["name"], 
        user=config["db"]["user"], 
        host=config["db"]["host"],
        password=config["db"]["password"],
        port=config["db"]["port"]
    )

    cursor = conn.cursor()
    
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS pdf_content (
            id SERIAL PRIMARY KEY,
            pdf_filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL
        )
    '''

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()