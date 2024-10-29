import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF

st.set_page_config(page_title="ChatPDF")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_save_file():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)

def similarity_score():
    st.sidebar.title("Sentence Similarity Score")
    with st.sidebar:
        source_sentence = st.text_input(label="Enter the golden answer:")

        if st.button("Compute Similarity Scores"):
            if not st.session_state["user_input"]:
                st.error("Please enter a source sentence")
            else:
                print("Response:")
                print(st.session_state["messages"][-1][0])
                score = st.session_state["assistant"].compute_similarity_score(
                    st.session_state["messages"][-1][0],
                    source_sentence
                )

                col1, col2= st.columns([1, 2])
                with col1:
                    st.write("Score")
                with col2:
                    st.write(f"{score:.2f}")


    st.markdown(
    """<style>
        .css-hi6a2p{border-bottom: 2px solid #6EB3D0;}
    </style>""",
    unsafe_allow_html=True
    )

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("ChatPDF")

    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,  #Cuando el valor del campo cambia, se borra la bd vectorial, retriever y chain
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

    similarity_score()

if __name__ == "__main__":
    page()