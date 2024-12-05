import pandas as pd
import psycopg2
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
    answer_correctness,
    answer_similarity
)

from src.code.generator import RAG

question_dataset_path = r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv"

try:
    conexion_bd = psycopg2.connect(
        database='rag',
        user='postgres',
        password='65ar99FA',
        host='localhost',
        port=1577
    )
    cursor = conexion_bd.cursor()
    cursor.execute("SELECT * FROM preguntas ORDER BY id LIMIT 2;")
    rows = cursor.fetchall()
    conexion_bd.commit()

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
        cursor.execute("SELECT * FROM preguntas ORDER BY id LIMIT 2;")
        rows = cursor.fetchall()

    rag = RAG(
        llm_model="granite3-dense",
        embedding_model="PlanTL-GOB-ES/roberta-base-bne",
        pdf_file_path=r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\BOE-A-2015-11430-consolidado.pdf",
    )

    #creamos nuestra RAG dataset para realizar la evaluación
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
                "reference": [referencia]
            }
        )

    rag_df = pd.DataFrame(rag_dataset)
    rag_eval_dataset = Dataset.from_pandas(rag_df)
    rag_eval_dataset.to_csv("basic_qa_ragas_dataset.csv")

    result = evaluate(
        rag_eval_dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevancy,
            context_recall,
            answer_correctness,
            answer_similarity
        ]
    )
    print(result)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)