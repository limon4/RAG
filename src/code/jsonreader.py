import json

import psycopg2

with open(r'C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\labourlawterminologyv2.jsonld', encoding='utf-8') as file:
    data = json.load(file)

conexion_bd = psycopg2.connect(
    database='rag',
    user='postgres',
    password='65ar99FA',
    host='localhost',
    port=1577
)
cursor = conexion_bd.cursor()

word = ''
synonyms = []
i = 0
aux = data[0]['@graph']
for elements in aux:
    keys = elements.keys()
    for key in keys:
        if key.endswith('prefLabel'):
            for terms in elements[key]:
                if terms['@language'] == 'es':
                    word = terms['@value']
        if key.endswith('altLabel'):
            for terms in elements[key]:
                if terms['@language'] == 'es':
                    synonyms.append(terms['@value'])

    if word != '' and len(synonyms) != 0:
        questions = []
        cursor.execute("SELECT id FROM preguntas WHERE pregunta LIKE %s;",
                       (('% ' + word + ' %'),))
        q_word = cursor.fetchall()
        for q in q_word:
            questions.append(q)
        cursor.execute("INSERT INTO sinonimos (palabra, sinonimos, pregunta_id) VALUES (%s, %s, %s);",
                       (word, i, questions))
        questions.clear()
        for synonym in synonyms:
            cursor.execute("SELECT id FROM preguntas WHERE pregunta LIKE %s;",
                           (('% ' + synonym + ' %'),))
            q_synonym = cursor.fetchall()
            for q in q_synonym:
                questions.append(q)
            cursor.execute("INSERT INTO sinonimos (palabra, sinonimos, pregunta_id) VALUES (%s, %s, %s);",
                           (synonym, i, questions))
            questions.clear()
        i += 1
        word = ''
        synonyms.clear()

conexion_bd.commit()
conexion_bd.close()