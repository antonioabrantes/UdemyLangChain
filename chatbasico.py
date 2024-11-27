import streamlit as st
from htmlTemplates import css, bot_template, user_template

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
open_api_token = os.getenv("OPENAI_API_TOKEN")

def main():
    st.set_page_config(page_title="Chatbot simples",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.header("Bem-vindo ao chatbot!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir histórico de mensagens
    ##for message in st.session_state.messages:
    ##    if message['role'] == "user":
    ##        with st.chat_message("user"):
    ##            st.markdown(message['content'])
    ##    else:
    ##        with st.chat_message("assistant"):
    ##            #st.markdown(message['content']['response'])
    ##            st.markdown(message['content'])
                
    for i, message in enumerate(st.session_state.messages):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message['content']), unsafe_allow_html=True)


    if "exit" not in st.session_state:
        st.session_state.exit = False

    # Verifica se o chatbot foi encerrado
    if st.session_state.exit:
        st.write("Chatbot: Até mais!")
        return
        
    # Configurar o modelo de linguagem OpenAI
    chat_model = ChatOpenAI(
        model="gpt-4o-mini",  # Modelo usado
        temperature=0.7,        # Controle de criatividade das respostas
        openai_api_key=open_api_token  # Substitua pela sua chave de API
    )
    #chat_model = ChatGroq(model="llama3-8b-8192", temperature=0.7) # o chatgroq não funciona histórico
    template = """
    Responda de forma sucinta em um parágrafo em português: {input}
    Histórico da conversa: {history}
    """
    prompt = ChatPromptTemplate.from_template(template=template)
    output_parser = StrOutputParser()
    chain = prompt | chat_model | output_parser
    
    # Configurar a memória para manter o histórico da conversa
    #memory = ConversationBufferMemory()

    # Criar a cadeia de conversação com o modelo e a memória
    #conversation = ConversationChain(
    #    llm=chat_model,
    #    memory=memory,
    #    prompt=prompt
    #)
    
    user_input = st.chat_input("Você: ",key='input1')
    if user_input is not None and user_input != '':
        user_question = {"role": "user", "content": user_input}
        st.session_state.messages.append(user_question)
        ##with st.chat_message("user"):
            ##st.markdown(user_input)
        st.write(user_template.replace("{{MSG}}", user_input), unsafe_allow_html=True)
    
        if user_input.lower() == "sair": 
            st.session_state.exit = True

        #response = conversation.invoke({"input":user_input})
        #st.write(st.session_state.messages)
        response = chain.invoke({"input":user_input,"history":st.session_state.messages})
        chatbot_response = {"role": "assistant", "content": response}
        st.session_state.messages.append(chatbot_response)
        #st.markdown(response['response'])
        ##st.markdown(response)
        st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)


if __name__ == '__main__':
    main()