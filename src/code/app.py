import pandas as pd
import psycopg2
from datasets import Dataset

from generator import RAG

conexion_bd = psycopg2.connect(
    database='rag',
    user='postgres',
    password='65ar99FA',
    host='localhost',
    port=1577
)
cursor = conexion_bd.cursor()
cursor.execute("SELECT * FROM preguntas ORDER BY id;")
rows = cursor.fetchall()
conexion_bd.commit()

question_dataset_path=r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv"
llm_model = "granite3-dense"
embedding_model="PlanTL-GOB-ES/roberta-base-bne"

if len(rows) == 0:
    question_dataset = pd.read_csv(
        question_dataset_path,
        usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD', 'Paragraph Spanish']
    )

    for i in range(len(question_dataset)):
        pregunta = question_dataset.iloc[i]['Question Spanish']
        respuesta = question_dataset.iloc[i]['Answer Spanish (highlight paragraph)\nBLACK BOLD']
        reference = question_dataset.iloc[i]['Paragraph Spanish']
        cursor.execute("INSERT INTO preguntas (pregunta, golden_answer, reference) VALUES (%s, %s, %s);",
                       (pregunta.strip(), respuesta.strip(), reference.strip()))

    conexion_bd.commit()
    cursor.execute("SELECT * FROM preguntas ORDER BY id;")
    rows = cursor.fetchall()

rag = RAG(
    llm_model=llm_model,
    embedding_model=embedding_model,
    pdf_file_path=r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\BOE-A-2015-11430-consolidado.pdf"
)

#creamos nuestro RAG dataset para realizar la evaluación
rag_dataset = []
for row in rows:
    pregunta_id = row[0]
    pregunta = row[1]
    respuesta_ref = row[2]
    referencia = row[3]
    respuesta_rag, contexto_rag = rag.ask(pregunta)

    rag_dataset.append(
        {
            "question": pregunta,
            "answer": respuesta_rag,
            "contexts": [contexto[0].page_content for contexto in contexto_rag],
            "ground_truths": [respuesta_ref],
            "reference": referencia
        }
    )

rag_df = pd.DataFrame(rag_dataset)
rag_eval_dataset = Dataset.from_pandas(rag_df)
rag_eval_dataset.to_csv(f"qa_ragas_dataset_{llm_model}_{embedding_model}.csv")