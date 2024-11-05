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
import psycopg2

LLM_MODEL = "mistral"
ST_MODEL = "Santp98/SBERT-pairs-bert-base-spanish-wwm-cased"
EMBEDDING_MODEL = "PlanTL-GOB-ES/RoBERTalex"
pdf_file_path = "/home/crodriguez/PycharmProjects/AI/RAG/src/resources/BOE-A-2015-11430-consolidado.pdf"
question_dataset_path = "/home/crodriguez/PycharmProjects/AI/RAG/src/resources/Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv"

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


def ingest():
    docs = PyPDFLoader(file_path=pdf_file_path).load()
    chunks = text_splitter.split_documents(docs)
    chunks = filter_complex_metadata(chunks)
    # embeddings = FastEmbedEmbeddings()
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    pdf_name = pdf_file_path.split("/")[-1].split(".")[0]
    suf = EMBEDDING_MODEL.split("/")[-1]
    persist_directory = fr"/home/crodriguez/PycharmProjects/AI/RAG/src/code/chroma_db_{pdf_name}_{suf}"

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
    retriever = ingest()
    chain = (
            {"context":retriever, "question":RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
    if not chain:
        return "Por favor inserte un documento PDF. "
    return chain.invoke(query)


try:
    conexion_bd = psycopg2.connect(
        database='rag',
        user='crodriguez',
        password='65ar99FA*!',
        host='localhost',
        port=5432
    )
    cursor = conexion_bd.cursor()
    cursor.execute("SELECT * FROM preguntas ORDER BY id;")
    rows = cursor.fetchall()
    conexion_bd.commit()
    if len(rows) == 0:
        question_dataset = pd.read_csv(
            question_dataset_path,
            usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD']
        )
        for i in range(len(question_dataset)):
            pregunta = question_dataset.iloc[i]['Question Spanish']
            respuesta = question_dataset.iloc[i]['Answer Spanish (highlight paragraph)\nBLACK BOLD']
            cursor.execute("INSERT INTO preguntas (pregunta, respuesta) VALUES (%s, %s);",
                           (pregunta.strip(), respuesta.strip()))
        conexion_bd.commit()

    for row in rows:
        id_q = row[0]
        question = row[1]
        golden_answer = row[2]
        rag_ans = ask(question)
        cursor.execute("INSERT INTO respuestas (pregunta_id, llm_model, embed_model, respuesta, score) VALUES (%i, %s, %s, %s, %.2f);",
                       (id_q, LLM_MODEL, EMBEDDING_MODEL, rag_ans, 0.0))
    conexion_bd.commit()
    conexion_bd.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)