import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.code.multi_query_retriever import MultiQueryRetriever


class RAG:

    def __init__(self, llm_model: str, embedding_model: str | None, pdf_file_path: str):

        self.pdf_file_path = pdf_file_path
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.vector_store = None

        #inicializamos el modelo generativo
        self.model = ChatOllama(model=llm_model)

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

        #creamos un template para el prompt que se le va a pasar al LLM
        self.prompt_template = PromptTemplate.from_template(
            """
            <s> [INST] Eres un asistente para tareas de respuesta a preguntas. Utiliza los siguientes elementos
            contextuales para responder a la pregunta. Si no sabes la respuesta, di simplemente que no lo sabes.
            Sé conciso en tu respuesta. [/INST] </s>
            [INST]Pregunta: {question}
            Contexto: {context}
            Respuesta: [/INST]
            """
        )


    def ingest(self):
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
                persist_directory=persist_directory
            )
        """
        self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        """



    def ask(self, query, expanded: bool = False):
        """
        Se realiza la pregunta deseada al modelo
        :param query: Pregunta que se quiere realizar
        :param expanded: Flag que indica si se desea expandir la pregunta o no
        :return: Devuelve la respuesta generada por el modelo
        """
        multi_query_retriever = MultiQueryRetriever(self.vector_store)

        if not expanded:
            context = multi_query_retriever.retriever_fun(query, 3)
        else:
            context = multi_query_retriever.run(query)['documents'][:3]

        context_text = "\n\n".join([doc.page_content for doc in context])

        prompt = self.prompt_template.format(question=query, context=context_text)
        answer = self.model.invoke(prompt)

        return answer.content, context
