import os.path

import torch.nn.functional
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pandas as pd
import mysql.connector

LLM_MODEL = "mistral"
ST_MODEL = "Santp98/SBERT-pairs-bert-base-spanish-wwm-cased"
EMBEDDING_MODEL = "PlanTL-GOB-ES/RoBERTalex"
pdf_file_path = r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\BOE-A-2015-11430-consolidado.pdf"

model = ChatOllama(model=LLM_MODEL)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=100
)

prompt = PromptTemplate.from_template(
    """
    <s> [INST] Eres un asistente para tareas de respuesta a preguntas. Utiliza los siguientes elementos
    contextuales para responder a la pregunta. Si no sabes la respuesta, di simplemente que no lo sabes.
    Sé conciso en tu respuesta. [/INST] </s>
    [INST]Pregunta: {question}
    Contexto: {context}
    Respuesta: [/INST]
    """
)


def ingest(pdf_file_path: str):
    docs = PyPDFLoader(file_path=pdf_file_path).load()
    chunks = text_splitter.split_documents(docs)
    chunks = filter_complex_metadata(chunks)
    # embeddings = FastEmbedEmbeddings()
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    pdf_name = pdf_file_path.split("\\")[-1].split(".")[0]
    persist_directory = fr"C:\Users\rodri\PycharmProjects\AI\RAG\src\code\chroma_db_{pdf_name}"

    if os.path.exists(persist_directory):
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vector_store.persist()

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5}
    )

    return retriever

def ask(query:str):
    retriever = ingest(pdf_file_path)
    chain = (
            {"context":retriever, "question":RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
    if not chain:
        return "Por favor inserte un documento PDF. "
    return chain.invoke(query)

question_dataset = pd.read_csv(
    r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv",
    usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD']
)

conexion_bd =mysql.connector.connect(host="localhost", user="root", passwd="INUBbKLu8j")
cursor = conexion_bd.cursor()

