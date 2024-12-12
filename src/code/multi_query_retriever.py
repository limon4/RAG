import psycopg2
from langchain_core.documents import Document


class MultiQueryRetriever:

    def __init__(self, vector_store):

        self.vector_db = vector_store
        self.docs = []
        self.results = []

    def _add_documents(self, document: tuple[Document, float]):
        if document[0] not in self.docs:
            self.docs.append(document[0])
            self.results.append(document)
        else:
            index = self.docs.index(document[0])
            if self.results[index][1] < document[1]:
                self.results[index] = document


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
                       "WHERE pregunta_id = (SELECT id FROM preguntas WHERE pregunta = %s LIMIT 1);",
                       (query,))
        rows = cursor.fetchall()
        conexion_bd.close()

        if len(rows) != 0:
            for row in rows:
                queries.append(row[0])

        for q in queries:
            result = self.vector_db.similarity_search_with_relevance_scores(q, 3)
            for doc in result:
                self._add_documents(doc)
        self.results.sort(key=lambda x: x[1], reverse=True)
        return self.results