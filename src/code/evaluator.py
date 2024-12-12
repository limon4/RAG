from datasets import Dataset
from evaluate import load
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness, answer_relevancy, context_recall
import pandas as pd

def eval_llm(llm_model: str, embedding_model: str | None, expanded: bool = False):
    references = []
    predictions = []
    if embedding_model is None:
        answer_dataset = pd.read_csv(
            fr".\qa_dataset\{llm_model}.csv",
            usecols=['answer', 'ground_truths']
        )
    elif expanded:
        answer_dataset = pd.read_csv(
            fr".\expanded_qa_ragas_dataset_{llm_model}_{embedding_model}.csv",
            usecols=['answer', 'ground_truths']
        )
    else:
        answer_dataset = pd.read_csv(
            fr".\qa_ragas_dataset_{llm_model}_{embedding_model}.csv",
            usecols=['answer', 'ground_truths']
        )

    for i in range(len(answer_dataset)):
        answer = answer_dataset.iloc[i]['answer']
        predictions.append(answer)
        ground_truth = answer_dataset.iloc[i]['ground_truths']
        references.append(ground_truth)

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

    data = {
        "llm": llm_model,
        "embedding_model": embedding_model,
        "Precision": avg_precision,
        "Recall": avg_recall,
        "F1": avg_f1
    }
    df = pd.DataFrame(data)
    eval_df = Dataset.from_pandas(df)
    if embedding_model is None:
        eval_df.to_csv(fr"evaluation\{llm_model}.csv")
    elif expanded:
        eval_df.to_csv(fr"evaluation\expanded_{llm_model}_{embedding_model}.csv")
    else:
        eval_df.to_csv(fr"evaluation\{llm_model}_{embedding_model}.csv")


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