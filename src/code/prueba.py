import os
import pandas as pd
import ast

from src.code.query_expander import QueryExpander

prev_directory = os.path.dirname(os.getcwd())
synonyms_csv = pd.read_csv(
    fr"{prev_directory}\resources\synonyms_list.csv",
    usecols=['palabra', 'sinonimos']
)

question_dataset = pd.read_csv(
    fr"{prev_directory}\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv",
    usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD']
)

questions_expanded = []
synonyms_list = {}
for i in range(len(synonyms_csv)):
    aux = synonyms_csv.iloc[i]
    synonyms_list[aux['palabra']] = ast.literal_eval(aux['sinonimos'])

query_expander = QueryExpander(synonyms_list)
for i in [0,1]:
    aux = question_dataset.iloc[i]
    original = aux['Question Spanish']
    ground_truth = aux['Answer Spanish (highlight paragraph)\nBLACK BOLD']
    combinations = query_expander.query_expansion(original)
    for expanded in combinations:
        print(' '.join(expanded))