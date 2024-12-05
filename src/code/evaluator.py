import psycopg2
from evaluate import load

LLM_MODEL = "granite3-dense"
EMBEDDING_MODEL = ""

conexion_bd = psycopg2.connect(
    database='rag',
    user='postgres',
    password='65ar99FA',
    host='localhost',
    port=1577
)
cursor = conexion_bd.cursor()
references = []
predictions = []
cursor.execute("SELECT golden_answer FROM preguntas ORDER BY id;")
ga = cursor.fetchall()
conexion_bd.commit()
for answer in ga:
    references.append(answer[0])
cursor.execute("SELECT respuesta FROM respuestas WHERE llm_model=%s AND embed_model=%s ORDER BY pregunta_id;",
               (LLM_MODEL, EMBEDDING_MODEL))
ans = cursor.fetchall()
conexion_bd.commit()
for answer in ans:
    predictions.append(answer[0])

bertscore = load("bertscore")
results = bertscore.compute(predictions=predictions, references=references, model_type="distilbert-base-uncased")
avg_precision = 0
for num in results['precision']:
    avg_precision += num
avg_precision /= 149
avg_recall = 0
for num in results['recall']:
    avg_recall += num
avg_recall /= 149
avg_f1 = 0
for num in results['f1']:
    avg_f1 += num
avg_f1 /= 149

cursor.execute("INSERT INTO metricas (llm_model, embed_model, precision, recall, f1) VALUES (%s, %s, %s, %s, %s);",
               (LLM_MODEL, EMBEDDING_MODEL, avg_precision, avg_recall, avg_f1))
conexion_bd.commit()
conexion_bd.close()