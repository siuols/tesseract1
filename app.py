import streamlit as st
import psycopg2

from database_operations import save_extracted_text
from pdf_handler import pdf_extract_text
from html_templates import css
from model import gpt_model
from utils import load_config

config = load_config()

def toggle_pdf_chat():
    st.session_state.pdf_chat = True
    clear_cache()

def clear_cache():
    st.cache_resource.clear()

def main():
    st.title("Chat bot")
    st.write(css, unsafe_allow_html=True)

    if "db_conn" not in st.session_state:
        st.session_state.db_conn = psycopg2.connect(
            database=config["db"]["name"], 
            user=config["db"]["user"], 
            host=config["db"]["host"],
            password=config["db"]["password"],
            port=config["db"]["port"]
        )
        st.session_state.new_session_key = None
    
    chat_container = st.container()
    
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload a pdf file",
        type=["pdf"],
        on_change=toggle_pdf_chat
    )
    
    if uploaded_pdf:
        with st.spinner("Processing pdf..."):
            filename, text = pdf_extract_text(uploaded_pdf.name)
            save_extracted_text(filename, text)

            generated_reply = gpt_model(text)

            with chat_container:
                with st.chat_message(
                    name="client",
                    avatar="chat_icons/bot_image.png"
                ):
                    st.write(generated_reply)
    
if __name__ == "__main__":
    main()