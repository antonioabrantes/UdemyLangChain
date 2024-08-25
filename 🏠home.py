import streamlit as st
import os
from dotenv import load_dotenv

#https://emojipedia.org/house

st.title('🏠Início ')
st.write("Inicialização da chave api...")

# coloque a chave em Setteing /secrets do streamlit.io

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
st.write(api_key)