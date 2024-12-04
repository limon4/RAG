import psycopg2

conexion_bd = psycopg2.connect(
    database='rag',
    user='postgres',
    password='65ar99FA',
    host='localhost',
    port=1577
)
cursor = conexion_bd.cursor()

cursor.execute("SELECT DISTINCT palabra, sinonimos, pregunta_id FROM sinonimos WHERE pregunta_id != '{}';")
rows = cursor.fetchall()
for row in rows:
    palabra = row[0]
    sinonimos_id = row[1]
    cursor.execute("SELECT palabra FROM sinonimos WHERE sinonimos = %s AND palabra != %s;",
                   (sinonimos_id, palabra))
    sinonimos = cursor.fetchall()
    pregunta_id = row[2]
    for question_id in pregunta_id:
        cursor.execute("SELECT pregunta, golden_answer, reference FROM preguntas WHERE id = %s;",
                       (question_id,))
        response = cursor.fetchall()[0]
        pregunta = response[0]
        golden_answer = response[1]
        reference = response[2]
        for sinonimo in sinonimos:
            aux = pregunta.replace(palabra, sinonimo[0])
            cursor.execute("INSERT INTO preguntas_extend (pregunta_id, pregunta, golden_answer, reference) VALUES (%s, %s, %s, %s);",
                           (question_id, aux, golden_answer, reference))

conexion_bd.commit()
conexion_bd.close()