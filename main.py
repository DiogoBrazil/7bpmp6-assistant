import time
import streamlit as st
import logging
from modules.GetAnswer import GetAnswer
from modules.message_alert import message_alert

logging.basicConfig(level=logging.INFO)

st.markdown(f"""
                    <div style='text-align: center;font-weight: bold; font-size: 24px;'>
                        <img src='https://thumbs2.imgbox.com/77/fd/vFIMHgar_t.jpeg' style='height: 100px;'/>  
                    </div>
                """, unsafe_allow_html=True)
st.markdown(f"""
                    <div style='text-align: center;font-weight: bold; font-size: 24px;'>
                        <h1>📝 Assistente do 7ºBPMP6</h1>  
                        <h6>🚀 Este é um chatbot que utiliza Inteligência Artificial Generativa para responder perguntas sobre a 
                            coletanea corrgepom 2015 CL 2 edição. Sinta-se à vontade para perguntar, porém lembre-se de que ele 
                            pode apresentar inconsistências nas respostas, por isso é importante avaliar cada uma delas. Uma dica é 
                            tentar ser bem específico na pergunta, pois quanto mais detalhes fornecer, melhor e mais precisa será a 
                            resposta.
                        </h6>
                    </div>
                """, unsafe_allow_html=True)
st.session_state.alert = False


def main():
    message_placeholder = st.empty()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    question = st.chat_input(
        "Pergunte algo sobre a coletanea corrgepom 2015 CL 2 edição:"
    )
    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Processando a resposta..."):
            thread = GetAnswer.create_thread(st.secrets['MESSAGE_FILE_ID'], question)
            response = GetAnswer.get_answer_with_assistant(thread.id, st.secrets['ASSISTANT_ID'])

            if not response:
                time.sleep(3)
                message_placeholder.error("Erro ao gerar resposta.")
                time.sleep(3)
                message_placeholder.empty()
                st.stop()
            else:
                time.sleep(3)
                message_placeholder.success("Resposta gerada com sucesso!")
                time.sleep(3)
                message_placeholder.empty()
                st.session_state.alert = True

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

    if st.session_state.alert:
        message_alert()


if __name__ == "__main__":
    main()
