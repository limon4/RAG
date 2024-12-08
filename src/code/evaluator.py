import psycopg2
from datasets import Dataset
from evaluate import load
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness, answer_relevancy, context_recall

LLM_MODEL = "granite3-dense"
EMBEDDING_MODEL = ""

def eval_llm():
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


def eval_rag(rag_eval_dataset, llm_model, embedding_model):
    result = evaluate(
        rag_eval_dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevancy,
            context_recall,
        ],
        llm=ChatOllama(model=llm_model),
        embeddings=HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    )
    dataset = Dataset.from_pandas(result.to_pandas())
    dataset.to_csv(f"results_{llm_model}_{embedding_model}.csv")