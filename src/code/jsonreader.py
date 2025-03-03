import json
import os

import pandas as pd

prev_directory = os.path.dirname(os.getcwd())

with open(rf'{prev_directory}/resources/labourlawterminologyv2.jsonld', encoding='utf-8') as file:
    data = json.load(file)

synonyms_list =[]
broader_dict = {}

i = 0
aux = data[0]['@graph']
#se recorre el json en busca de las palabras y sus términos relacionados en español
for elements in aux:
    word = ''
    synonyms = []
    lt = ''
    keys = elements.keys()
    for key in keys:
        if key.endswith('prefLabel'):
            for terms in elements[key]:
                if terms['@language'] == 'es':
                    word = terms['@value'].lower()
        if key.endswith('altLabel'):
            for terms in elements[key]:
                if terms['@language'] == 'es':
                    synonyms.append(terms['@value'].lower())
        if key.endswith('broader'):
            lt = elements[key][0]['@id']

    #si hay una palabra con sinónimos en español se almacena en un fichero csv
    if word != '' and len(synonyms) != 0:
        result_word = {
            "palabra": word,
            "sinonimos": synonyms,
            "broader": lt
        }
        synonyms_list.append(result_word)
        broader_dict[elements['@id']] = [word] + synonyms
    elif word != '':
        broader_dict[elements['@id']] = [word]
    elif len(synonyms) != 0:
        broader_dict[elements['@id']] = synonyms


df = pd.DataFrame(synonyms_list)
synonyms_list.clear()
for i in range(len(df)):
    aux = df.iloc[i]
    new_synonyms = aux['sinonimos']
    if aux['broader'] != '':
        word_list = broader_dict[aux['broader']]
        new_synonyms += word_list
    sol = {
        "palabra": aux['palabra'],
        "sinonimos": new_synonyms
    }
    synonyms_list.append(sol)
df2 = pd.DataFrame(synonyms_list)
csv_path = fr"{prev_directory}/resources/synonyms_list.csv"
df2.to_csv(csv_path)