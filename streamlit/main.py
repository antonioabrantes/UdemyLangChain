import streamlit as st
import time
import pandas as pd

def main():
    st.title("Título Novo")
    st.write("alguns exemplos de uso")

    st.header("Input de texto")
    texto = st.text_input("Digite aqui:")
    if texto:
        st.write("Texto: ",texto)

    st.header("Selectbox")
    texto = st.selectbox("Selecione:",['op1','op2','op3'])
    if texto:
        st.write("Opção: ",texto)

    st.header("Checkbox")
    valor = st.checkbox("Marque:")
    st.write("Checkbox ativado: ",valor)

    st.header("Botão")
    if st.button("Clique aqui"):
        st.write("você clicou no botão")

    st.header("loading...")
    with st.spinner("Aguarde.."):
        time.sleep(3)
        st.write("encerrado")
        st.success("carregado com sucesso")

    st.header("upload de arquivo")
    arquivo = st.file_uploader("Escolha arquivo", type=['pdf','txt'])
    if arquivo:
        st.write("Nome do arquivo: ",arquivo.name)

    df = pd.read_csv("my_data.csv")
    st.line_chart(df)


main()