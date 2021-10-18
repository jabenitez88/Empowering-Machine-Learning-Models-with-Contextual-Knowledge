# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 18:12:08 2021

@author: MICROSOFT
"""

import requests
import json
import pandas as pd
import csv
import time
import re

from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs import KG
from pyrdf2vec.walkers import RandomWalker


df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2b.csv', sep=';',error_bad_lines=False)
#df = pd.read_csv('data\ed-dataset.csv', sep=';',error_bad_lines=False)


print(df.head)
print(df.text_orig)

tw_list = df['text_orig'].tolist()
resp_list = df['falcon2_responses'].tolist()


# %% 2

responses_entities_instances = []
responses_entities_labels = []

resp_entities_labels = []
resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

for resp in resp_list:
    resp_entities_labels = []
    resp_entities_instances = []
    try:
        result=json.loads(resp)
        if len(result['entities_wikidata']) > 0:
            #print(result['entities_wikidata'])
            for entity in result['entities_wikidata']:
                entity_instance = entity[0].replace('>','').replace('<','')
                entity_label = entity[1].replace('>','').replace('<','')
                resp_entities_instances.append(entity_instance)
                resp_entities_labels.append(entity_label)
                if (entity_instance in all_entities_instances) is False:
                    all_entities_instances.append(entity_instance)
                    all_entities_labels.append(entity_label)
        responses_entities_instances.append(resp_entities_instances)
        responses_entities_labels.append(resp_entities_labels)
    except ValueError:
        print("No entities")
        responses_entities_instances.append(['No entity'])
        responses_entities_labels.append(['No entity'])

df['entities_instances_wikidata'] = responses_entities_instances
df['entities_labels_wikidata'] = responses_entities_labels

print(len(all_entities_labels))
print(len(all_entities_instances))





# %%

entities = all_entities_instances
transformer = RDF2VecTransformer(
    Word2Vec(epochs=10),
    walkers=[RandomWalker(4, 10, with_reverse=False, n_jobs=2)],
    verbose=1
)
embeddings, literals = transformer.fit_transform(
    KG(
        "https://query.wikidata.org/sparql"
    ),
    entities
)

# Recursos que son de la misma clase
print(embeddings)
# [
#     array([ 1.5737595e-04,  1.1333118e-03, -2.9838676e-04,  ..., -5.3064007e-04,
#             4.3192197e-04,  1.4529384e-03], dtype=float32),
#     array([-5.9027621e-04,  6.1689125e-04, -1.1987977e-03,  ...,  1.1066757e-03,
#            -1.0603866e-05,  6.6087965e-04], dtype=float32),
#     array([ 7.9996325e-04,  7.2907173e-04, -1.9482171e-04,  ...,  5.6251377e-04,
#             4.1435464e-04,  1.4478950e-04], dtype=float32)
# ]

print(literals)