import streamlit as st
import logging
from openai import OpenAI

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])


class GetAnswer:
    def __init__(self):
        pass

    @staticmethod
    def create_thread(message_file_id, question):
        try:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "attachments": [
                            {"file_id": message_file_id, "tools": [{"type": "file_search"}]}
                        ],
                    }
                ]
            )
            return thread
        except Exception as e:
            logging.error(f"Erro ao criar thread: {e}")
            return False

    @staticmethod
    def get_answer_with_assistant(thread_id, assistant_id):
        try:
            # Use the create and poll SDK helper to create a run and poll the status of
            # the run until it's in a terminal state.

            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id, assistant_id=assistant_id
            )

            messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))

            message_content = messages[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
                if file_citation := getattr(annotation, "file_citation", None):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(f"[{index}] {cited_file.filename}")

            return f'{message_content.value}\n\n{"".join(citations)}'
            # print(message_content.value)
            # print("\n".join(citations))

        except Exception as e:
            logging.error(f"Erro ao gerar resposta: {e}")
            return False
