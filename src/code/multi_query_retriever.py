import os

import pandas as pd
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

        prev_directory = os.path.dirname(os.getcwd())
        expanded_questions_dataset = pd.read_csv(
            fr"{prev_directory}\resources\expanded_questions.csv",
            usecols=['original', 'expandida']
        )

        for i in range(len(expanded_questions_dataset)):
            aux = expanded_questions_dataset.iloc[i]
            if aux['original'] == query:
                queries.append(aux['expandida'])

        for q in queries:
            result = self.vector_db.similarity_search_with_relevance_scores(q, 3, score_threshold=0.5)
            for doc in result:
                self._add_documents(doc)
        self.results.sort(key=lambda x: x[1], reverse=True)
        return self.results