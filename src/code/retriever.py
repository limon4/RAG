import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Retriever:

    def __init__(self, pdf_file_path: str, embedding_model: str | None):

        self.pdf_file_path = pdf_file_path
        self.vector_store = None
        self.embedding_model = embedding_model

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=100
        )

        #inicializamos el modelo para el cálculo de embeddings
        self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': False}
        )


    def _ingest(self):
        """
        Realiza la ingesta del fichero indicado en la variable pdf_file_path.

        El proceso llevado a cabo es el siguiente:
            1. Se obtiene el texto obtenido de la ruta pdf_file_path.
            2. El texto se divide en chunks según lo especificado en la variable text_splitter.
            3. Se calcula el embedding de los chunks en caso de que no se haya calculado previamente.
            4. Los vectores calculados se almacenan en una base de datos vectorial.
        :return: Se devuelve el recuperador asociado a la base de datos
        """
        docs = PyPDFLoader(file_path=self.pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        # embeddings = FastEmbedEmbeddings()
        pdf_name = self.pdf_file_path.split("\\")[-1].split(".")[0]
        suf = self.embedding_model.split("/")[-1]
        persist_directory = fr"C:\Users\rodri\PycharmProjects\AI\RAG\src\code\chroma_db_{pdf_name}_{suf}"

        if os.path.exists(persist_directory):
            self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        else:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=persist_directory,
                collection_metadata={"hnsw:space": "cosine"}
            )
        """self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )"""

        return self.vector_store

    def retriever(self, query: str, k: int = 3):
        vector_store_retriever = self._ingest()
        return vector_store_retriever.similarity_search_with_relevance_scores(query, k)