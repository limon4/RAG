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
        result_word = {
            "palabra": word,
            "sinonimos": synonyms
        }
        synonyms_list.append(result_word)

df = pd.DataFrame(synonyms_list)
csv_path = fr"{prev_directory}\resources\synonyms_list.csv"
df.to_csv(csv_path)