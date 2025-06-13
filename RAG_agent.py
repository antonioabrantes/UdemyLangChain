# streamlit run RA_agent.py
# selecione lei.pdf
# pergunte: os direitos da personalidade são intransmissíveis?

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import AgentExecutor, create_tool_calling_agent

import os
load_dotenv(dotenv_path='.env',override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def pdf_read(pdf_doc):
    text = ""
    for pdf in pdf_doc:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def vector_store(text_chunks):
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_db")

def get_conversational_chain(tools,question):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=openai_api_key)
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
            """Você é um assistente útil. Responda à pergunta o mais detalhadamente possível a partir do contexto fornecido, certifique-se de fornecer todos os detalhes, se a resposta não estiver no contexto fornecido, diga apenas "a resposta não está disponível no contexto", não forneça a resposta errada""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
    )
    tool=[tools]
    agent = create_tool_calling_agent(llm, tool, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)
    response=agent_executor.invoke({"input": question, "chat_history":[] })
    print(response)
    st.write("Resposta: ", response['output'])

def user_input(user_question):
    new_db = FAISS.load_local("faiss_db", embeddings,allow_dangerous_deserialization=True)
    retriever=new_db.as_retriever()
    retrieval_chain= create_retriever_tool(retriever,"pdf_extractor","Esta ferramenta fornece respostas a partir do PDF")
    get_conversational_chain(retrieval_chain,user_question)

def main():
    st.set_page_config("Chat PDF")
    st.header("RAG baseado em PDF")

    user_question = st.text_input("Faça sua pergunta ao arquivo PDF")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_doc = st.file_uploader("Faça o upload dos arquivos PDF e pressione o Botão Processar", accept_multiple_files=True)
        if st.button("Processar"):
            with st.spinner("Processando..."):
                raw_text = pdf_read(pdf_doc)
                #st.write(raw_text)
                text_chunks = get_chunks(raw_text)
                vector_store(text_chunks)
                st.success("Feito")

if __name__ == "__main__":
    main()