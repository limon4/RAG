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


class ChatPDF:
    vector_store = None
    retriever = None
    chain = None
    LLM_MODEL = "mistral"
    ST_MODEL = "Santp98/SBERT-pairs-bert-base-spanish-wwm-cased"
    EMBEDDING_MODEL = "PlanTL-GOB-ES/roberta-base-bne"

    def __init__(self):
        self.model = ChatOllama(model=self.LLM_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=100
        )
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] Eres un asistente para tareas de respuesta a preguntas. Utiliza los siguientes elementos
            contextuales para responder a la pregunta. Si no sabes la respuesta, di simplemente que no lo sabes.
            Sé conciso en tu respuesta. [/INST] </s>
            [INST]Pregunta: {question}
            Contexto: {context}
            Respuesta: [/INST]
            """
        )

    def ingest(self, pdf_file_path:str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        #embeddings = FastEmbedEmbeddings()
        embeddings = HuggingFaceEmbeddings(
            model_name=self.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        pdf_name = pdf_file_path.split("\\")[-1].split(".")[0]
        persist_directory = fr"C:\Users\rodri\PycharmProjects\AI\RAG\src\code\chroma_db_{pdf_name}"

        if os.path.exists(persist_directory):
            self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        else:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=persist_directory
            )
            self.vector_store.persist()

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k":3, "score_threshold":0.5}
        )
        self.chain = (
            {"context":self.retriever, "question":RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
        )

    def ask(self, query:str):
        if not self.chain:
            return "Por favor inserte un documento PDF. "
        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def compute_similarity_score(self, rag_answer, golden_answer):
        model = SentenceTransformer(self.ST_MODEL)
        ra_embedding = model.encode([rag_answer], convert_to_tensor=True)
        ga_embedding = model.encode([golden_answer], convert_to_tensor=True)
        cosine_similarities = torch.nn.functional.cosine_similarity(ra_embedding, ga_embedding)
        return cosine_similarities.item()