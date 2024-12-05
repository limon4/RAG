import psycopg2
from langchain_core.documents import Document


class MultiQueryRetriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store
        self.results = []

    def add_documents(self, document: Document):
        if document not in self.results:
            self.results.append(document)

    def run(self, query):
        """
        :param query: Query para la que se desea obtener los documentos relevantes.
        :return: Devuelve un diccionario con la lista de documentos relevantes.
        La clave del diccionario es 'documents'.
        """
        queries = [query]

        conexion_bd = psycopg2.connect(
            database='rag',
            user='postgres',
            password='65ar99FA',
            host='localhost',
            port=1577
        )
        cursor = conexion_bd.cursor()
        cursor.execute("SELECT pregunta "
                       "FROM preguntas_extend "
                       "WHERE pregunta_id = (SELECT id FROM preguntas WHERE pregunta = %s);",
                       (query,))
        rows = cursor.fetchall()
        conexion_bd.close()

        if len(rows) != 0:
            for row in rows:
                queries.append(row[0])

        for q in queries:
            result = self.retriever_fun(q, 3)
            for doc in result:
                self.add_documents(doc)
        self.results.sort(key=lambda x: x.metadata['score'], reverse=True)
        return {"documents": self.results}