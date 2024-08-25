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

# requirements.txt
# streamlit
# python-dotenv
# langchain 
# langchain-openai
# langchain-groq

### Udemy Aula 2: acesso a llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain_groq import ChatGroq

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

topico = st.text_input('Entre com sua pergunta')

if topico:
    #llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", max_tokens=256, openai_api_key=openai_api_key)
    llm = ChatGroq(temperature=0.0, model="llama3-8b-8192", max_tokens=256)
    chain = llm | StrOutputParser()
    #resposta = llm.invoke(topico)
    resposta = chain.invoke(topico)
    st.write(resposta)
    
