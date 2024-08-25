# Udemy Aula 1 - Inicialização no streamlit, githubdesktop e githubdesktop

import streamlit as st
import os
from dotenv import load_dotenv

#https://emojipedia.org/house

st.title('🏠Início ')
st.write("Inicialização da chave api...")

# coloque a chave em Setting /secrets do streamlit.io

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
#st.write(openai_api_key)


### Udemy Aula 2: acesso a llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

topico = st.text_input('Entre com sua pergunta')

if topic:
    llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", max_tokens=256, openai_api_key=openai_api_key)
    resposta = llm.invoke(topico)
    st.write(resposta)