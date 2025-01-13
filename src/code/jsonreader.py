import json
import os

import pandas as pd

prev_directory = os.path.dirname(os.getcwd())

with open(rf'{prev_directory}\resources\labourlawterminologyv2.jsonld', encoding='utf-8') as file:
    data = json.load(file)

synonyms_list =[]

i = 0
aux = data[0]['@graph']
#se recorre el json en busca de las palabras y sus términos relacionados en español
for elements in aux:
    word = ''
    synonyms = []
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

    #si hay una palabra con sinónimos en español se almacena en un fichero csv
    if word != '' and len(synonyms) != 0:
        question_dataset = pd.read_csv(
            fr"{prev_directory}\resources\Cuatrecasas-OEG-Spanish Workers Statute Eval Dataset.xlsx - 1st set.csv",
            usecols=['Question Spanish', 'Answer Spanish (highlight paragraph)\nBLACK BOLD', 'Paragraph Spanish']
        )
        questions = []
        synonyms.append(word)
        index_per_word = {synonym: [] for synonym in synonyms}
        for j in range(len(question_dataset)):
            question = question_dataset.iloc[j]['Question Spanish'].lower()
            found_word = None
            for synonym in synonyms:
                if (len(synonym.split()) > 1 and synonym.lower() in question) or (synonym.lower() in question.lower().split()):
                    if found_word is None or found_word in synonym:
                        found_word = synonym

            if found_word:
                index_per_word[found_word].append(j)

        for synonym, index in index_per_word.items():
            result_word = {
                "palabra": synonym,
                "sinonimos": i,
                "pregunta_id": index
            }
            synonyms_list.append(result_word)
        i+=1


df = pd.DataFrame(synonyms_list)
csv_path = fr"{prev_directory}\resources\synonyms_list.csv"
df.to_csv(csv_path)