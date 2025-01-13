import ast
import os
import pandas as pd

prev_directory = os.path.dirname(os.getcwd())
synonyms_list = pd.read_csv(
    fr"{prev_directory}\resources\synonyms_list.csv",
    usecols=['palabra', 'sinonimos', 'pregunta_id']
)

question_dataset = pd.read_csv(
    fr"{prev_directory}\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv",
    usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD']
)

questions_expanded = []
for i in range(len(synonyms_list)):
    aux = synonyms_list.iloc[i]
    if aux['pregunta_id'] != '[]':
        word = aux['palabra']
        synonyms_id = aux['sinonimos']
        questions = ast.literal_eval(synonyms_list.iloc[i]['pregunta_id'])
        j = i
        while j != 0 and synonyms_list.iloc[j-1]['sinonimos'] == synonyms_id:
            j -= 1
        while synonyms_list.iloc[j]['sinonimos'] == synonyms_id:
            if j != i:
                synonym = synonyms_list.iloc[j]['palabra']
                for question_id in questions:
                    question = question_dataset.iloc[question_id]['Question Spanish'].lower()
                    question_expanded = question.replace(word, synonym)
                    ground_truth = question_dataset.iloc[question_id]['Answer Spanish (highlight paragraph)\nBLACK BOLD']
                    expanded = {
                        "id_original": question_id,
                        "original": question,
                        "expandida": question_expanded,
                        "ground_truth": ground_truth
                    }
                    questions_expanded.append(expanded)
            j += 1

df = pd.DataFrame(questions_expanded)
csv_path = fr"{prev_directory}\resources\expanded_questions.csv"
df.to_csv(csv_path)