#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 22:41:27 2021

@author: jabenitez
"""


import requests
import json
import pandas as pd
import csv
import time
import re
import os
from ast import literal_eval
import matplotlib.pyplot as plt


from pathlib import Path


#%% 2
#my_path = os.path.abspath(os.path.dirname(__file__))
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-entities-reduced.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False, 
                 converters={'entities_instances_wikidata_cleaned':literal_eval,
                             'entities_labels_wikidata_cleaned':literal_eval})




# ed-spacy-entities-count-reduced.csv
# ed-spacy-entities-count-reduced2.csv
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-entities-reduced2.csv'
dfS = pd.read_csv(path, sep=';',error_bad_lines=False, 
                  converters={'spacy_entities_ids':literal_eval,
                              'spacy_entities_labels':literal_eval,
                              'spacy_entities_urls':literal_eval})


resp_list = dfS['spacy_entities_ids'].tolist()

print(resp_list[65])

for idx, resp in enumerate(resp_list):
    for idx2, enti in enumerate(resp):
        if((enti is not None) and (enti is not '')):
            resp_list[idx][idx2] = 'http://www.wikidata.org/entity/Q'+str(enti)
            

dfS['spacy_entities_ids'] = resp_list
dfS['entities_instances_wikidata_cleaned'] = df['entities_instances_wikidata_cleaned'].tolist()
dfS['entities_labels_wikidata_cleaned'] = df['entities_labels_wikidata_cleaned'].tolist()


dfS['falcon_spacy_entities'] = dfS['spacy_entities_ids'] + dfS['entities_instances_wikidata_cleaned']

dfS['falcon_spacy_labels'] = dfS['spacy_entities_labels'] + dfS['entities_labels_wikidata_cleaned']
dfS['falcon_spacy_labels'] = dfS['falcon_spacy_labels'].apply(lambda x: list(set(x)))


dfS['falcon_spacy_entities'] = dfS['falcon_spacy_entities'].apply(lambda x: list(set(x)))

path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2.csv'

dfS.to_csv(path,sep=';')

# %% 3

responses_entities_instances = []
responses_entities_labels = []

total_resp_entities_labels = []
total_resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

all_entities_ids = []
all_entities_labels_a = []
all_entities_instances_a = []

resp_list = dfS['falcon_spacy_entities'].tolist()
resp_labels = dfS['falcon_spacy_labels'].tolist()


for idx1,resp in enumerate(resp_list):
    
    for idx2,enti in enumerate(resp):
        if((enti is not None) and (enti is not '')):
            if(enti in all_entities_instances) is False:
               all_entities_instances.append(enti)
               if(idx2 < len(resp_labels[idx1])):
                   all_entities_labels.append(resp_labels[idx1][idx2])
               else:
                   all_entities_labels.append(enti)

#%%

dfUniques = pd.DataFrame({'entity':all_entities_instances,'label':all_entities_labels})
dfUniques.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-entities-uniques.csv',sep=';')



# %%


print(dfS['falcon_spacy_entities'][4][0])
# %% 

df_orig = dfS.copy()
df_b = pd.DataFrame(dfS['falcon_spacy_entities'])

# %%

print(df_b['falcon_spacy_entities'][4][0])

# %% 6

s = df_b.iloc[:,0]

t = pd.get_dummies(s.apply(pd.Series).stack()).sum(level=0)
# %% 7

df_c = df_b.falcon_spacy_entities.str.join('|').str.get_dummies()


# %% 8

print(df_c.head())


# %%
from sklearn.metrics.pairwise import pairwise_distances
jac_sim = 1 - pairwise_distances(df_c, metric = "hamming")
# optionally convert it to a DataFrame
jac_sim = pd.DataFrame(jac_sim, index=df_c.index, columns=df_c.index)

jac_sim.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-jaccard.csv',sep=';')
# %%

print(jac_sim.values.reshape(-1))

# %%

import numpy as np


n=4000000
x = jac_sim.values.reshape(-1)
y = 0.0 + 0.0 * x + 1000 * np.random.standard_normal(n)
plt.hexbin(x,y)

plt.show()

# pd.plotting.scatter_matrix(jac_sim, diagonal='kde')

#pd.plotting.scatter_matrix(jac_sim, alpha=0.2)
#