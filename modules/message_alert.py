import streamlit as st


def message_alert():
    url = "https://api.whatsapp.com/send?phone=69999749201&text=Olá%2C+Gostaria+de+reportar+uma+inconsistência+nas+respostas+de+sua+aplicação%21+"
    texto_link = 'Reportar inconstência na resposta'

    return st.markdown(f"[{texto_link}]({url})")
