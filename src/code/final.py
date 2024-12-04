import pandas as pd
import psycopg2
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas import EvaluationDataset
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate

from src.code.rag import RAG

question_dataset_path=r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv"

rag = RAG(
    llm_model="granite3-dense",
    embedding_model="PlanTL-GOB-ES/roberta-base-bne",
    pdf_file_path=r"C:\Users\rodri\PycharmProjects\AI\RAG\src\resources\BOE-A-2015-11430-consolidado.pdf",
)

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

    rag.ingest()

    bool_rag = True  # indica si el rag está activado o no
    if bool_rag:
        cursor.execute("SELECT * FROM respuestas WHERE llm_model = %s AND embed_model = %s",
                       (rag.llm_model, rag.embedding_model))
    else:
        cursor.execute("SELECT * FROM respuestas WHERE llm_model = %s AND embed_model = %s",
                       (rag.llm_model, ''))
    aux = cursor.fetchall()
    conexion_bd.commit()

    if len(aux) == 0:
        queries = []
        ground_truths = []
        answers = []
        contexts = []
        for row in rows:
            id_q = row[0]
            question = row[1]
            queries.append(question)
            golden_answer = row[2]
            ground_truths.append(golden_answer)

            if bool_rag:
                rag_ans, rag_context = rag.ask(question)
                contexts.append([context.page_content for context in rag_context])
            else:
                rag_ans = rag.model.invoke(question).content
                EMBEDDING_MODEL = ''

            answers.append(rag_ans)

            #cursor.execute("INSERT INTO respuestas (pregunta_id, llm_model, embed_model, respuesta) VALUES (%s, %s, %s, %s);",
            #               (id_q, rag.llm_model, rag.embedding_model, rag_ans))
            print(f"Se ha ingestado la respuesta a la pregunta {id_q}")

        data = {
            "question": queries,
            "answer": answers,
            "contexts": contexts,
            "ground_truths": ground_truths
        }

        eval_dataset = EvaluationDataset.from_dict(data)
        evaluator_llm = LangchainLLMWrapper(rag.model)
        evaluator_embedding = LangchainEmbeddingsWrapper(rag.embeddings)

        metrics = [
            LLMContextRecall(llm=evaluator_llm),
            FactualCorrectness(llm=evaluator_llm),
            Faithfulness(llm=evaluator_llm),
            SemanticSimilarity(embeddings=evaluator_embedding)
        ]
        results = evaluate(dataset=eval_dataset, metrics=metrics).scores
        print(results)

        print("Se han ingestado todas las respuestas")
        conexion_bd.commit()
        conexion_bd.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)