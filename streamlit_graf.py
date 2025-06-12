#pip install streamlit
#streamlit run streamlit_graf.py

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
#from main_embedding import chat_gen

load_dotenv(".env",override=True)
#openai_api_key = os.environ['OPENAI_API_KEY']
openai_api_key = os.getenv("OPENAI_API_KEY")

#@st.cache_resource
#def initialize():
#    chat= chat_gen()
#    return chat

#st.session_state.chat=initialize()

st.title("Gráfico de vendas")
st.markdown(
"""
<img src="https://cientistaspatentes.com.br/imagens/IARA.png" width="140"/>
""", 
unsafe_allow_html=True
)
st.markdown("<small>Olá eu sou assistente virtual auxiliar sobre o estoque de vendas dos produtos da loja de 2020 a 2024. Por exemplo: monte grafico de vendas de sapatos de 2020 a 2024", unsafe_allow_html=True)

# https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization

#if 'step' not in st.session_state:
#    st.session_state['step'] = 0

context = '{"patents":[{"vendas":"total","normal":{"2020":4169,"2021":5186,"2022":6067,"2023":6312,"2024":7022},"natal":{"2020":1127,"2021":1126,"2022":1201,"2023":1687,"2024":511}},{"vendas":"sapatos","normal":{"2020":170,"2021":240,"2022":320,"2023":328,"2024":379},"natal":{"2020":59,"2021":36,"2022":21,"2023":87,"2024":5}},{"vendas":"camisas","normal":{"2020":299,"2021":418,"2022":482,"2023":489,"2024":521},"natal":{"2020":52,"2021":46,"2022":94,"2023":136,"2024":35}},{"vendas":"bolsas","normal":{"2020":270,"2021":365,"2022":455,"2023":492,"2024":520},"natal":{"2020":53,"2021":49,"2022":70,"2023":110,"2024":47}},{"vendas":"fogões","normal":{"2020":207,"2021":263,"2022":301,"2023":331,"2024":366},"natal":{"2020":57,"2021":50,"2022":36,"2023":51,"2024":7}},{"vendas":"telefones","normal":{"2020":182,"2021":241,"2022":298,"2023":279,"2024":277},"natal":{"2020":32,"2021":70,"2022":56,"2023":103,"2024":53}},{"vendas":"televisores","normal":{"2020":395,"2021":515,"2022":596,"2023":643,"2024":669},"natal":{"2020":67,"2021":106,"2022":94,"2023":118,"2024":51}},{"vendas":"computadores","normal":{"2020":196,"2021":218,"2022":253,"2023":264,"2024":302},"natal":{"2020":26,"2021":58,"2022":16,"2023":31,"2024":1}},{"vendas":"microfones","normal":{"2020":228,"2021":371,"2022":490,"2023":553,"2024":619},"natal":{"2020":80,"2021":57,"2022":72,"2023":129,"2024":33}},{"vendas":"teclados","normal":{"2020":0,"2021":0,"2022":0,"2023":0,"2024":0},"natal":{"2020":9,"2021":4,"2022":0,"2023":0,"2024":0}},{"vendas":"saias","normal":{"2020":281,"2021":370,"2022":421,"2023":486,"2024":562},"natal":{"2020":38,"2021":46,"2022":69,"2023":66,"2024":49}},{"vendas":"óculos","normal":{"2020":180,"2021":251,"2022":402,"2023":489,"2024":557},"natal":{"2020":123,"2021":45,"2022":27,"2023":35,"2024":0}},{"vendas":"skates","normal":{"2020":149,"2021":168,"2022":199,"2023":166,"2024":162},"natal":{"2020":111,"2021":75,"2022":67,"2023":74,"2024":38}}}]}'

chat_history=[]
llm = ChatOpenAI(openai_api_key=openai_api_key,
                    temperature=0.0,
                    max_tokens=4000,
                    model="gpt-4o-mini"
                    )

# Define your system instruction
system_instruction = """ 
Você é um assistente virtual. Sua função será responder as perguntas com base nos dados fornecidos.
Você deve buscar se comportar de maneira cordial e solícita.

Encerre com o cabeçalho:
Atenciosamente,
Equipe Fale Conosco
"""

# Define your template with the system instruction
template = (
    f"{system_instruction} "
    "Combine o histórico {chat_history} "
    "Aqui está a dúvida recebida {question}"
    "Aqui está o contexto de respostas anteriores recebidas de requerentes feitas pelo nosso time do Fale Conosco {context}. "
    "Escreva a melhor resposta para solucionar a dúvida apresentada pelo requerente."
)

prompt = PromptTemplate(input_variables=['context','question','chat_history'],template=template)
chain = prompt | llm

template2 = (
    "Aqui está a dúvida recebida {question}"
    "Aqui está o contexto de respostas anteriores recebidas de requerentes feitas pelo nosso time do Fale Conosco {context}. "
    "Escreva a resposta sucinta."
)

prompt2 = PromptTemplate(input_variables=['context','question'],template=template2)
chain2 = prompt2 | llm

if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ''

if 'response' not in st.session_state:
    st.session_state['response'] = ''

if 'similar_response' not in st.session_state:
    st.session_state['similar_response'] = ''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0

# Display chat messages from history on app rerun
#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.markdown(message["content"])

if st.session_state.step == 0:
    if prompt := st.text_area("Entre com sua pergunta abaixo."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.prompt = prompt

        response = chain.invoke({
            "context": context,
            "question": prompt,
            "chat_history": chat_history
        })
        chat_history.append((prompt, response.content))
        st.session_state.response = response

        with st.chat_message("assistant"):
            st.markdown(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        prompt_modificado = f"Escreva um código Python que gere um gráfico mostrando " + prompt + ". Mostre apenas os comandos do código."
        response = chain2.invoke({
            "context": context,
            "question": prompt_modificado
        })
        #st.markdown(response.content)
        comando = response.content
        comando = comando.replace("```","")
        comando = comando.replace("python","")
        st.markdown("Imprimindo gráfico...")
        # st.markdown(comando)
        try:
            exec(comando)
            st.pyplot(plt.gcf())
        except Exception as e:
            st.markdown(f"Ocorreu um erro ao executar o código : {e}")
        
