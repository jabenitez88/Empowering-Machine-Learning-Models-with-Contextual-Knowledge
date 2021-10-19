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
path = '../data/ed-dataset-falcon2-lists-cleaned.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False, converters={'entities_instances_wikidata_cleaned':literal_eval,'entities_labels_wikidata_cleaned':literal_eval})





path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-entities-reduced.csv'
dfS = pd.read_csv(path, sep=';',error_bad_lines=False, converters={'spacy_entities_ids':literal_eval,'spacy_entities_labels':literal_eval,'spacy_entities_urls':literal_eval})

# %% 3

responses_entities_instances = []
responses_entities_labels = []

total_resp_entities_labels = []
total_resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

all_entities_labels_a = []
all_entities_instances_a = []

resp_list = df['spacy_entities_urls'].replace('https','http').replace('wiki/','entity/').tolist()

for resp in resp_list:
    
    for enti in resp:
        if(enti in all_entities_instances) is False:
            all_entities_instances.append(enti)

# %%

responses_entities_instances = []
responses_entities_labels = []

total_resp_entities_labels = []
total_resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

all_entities_labels_a = []
all_entities_instances_a = []

resp_list = df['entities_instances_wikidata_cleaned'].tolist()

for resp in resp_list:
    
    for enti in resp:
        if(enti in all_entities_instances) is False:
            all_entities_instances.append(enti)
    

# %%


print(df['entities_instances_wikidata_cleaned'][4][0])
# %% 

df_orig = df.copy()
df_b = pd.DataFrame(df['entities_instances_wikidata_cleaned'])

# %%

print(df_b['entities_instances_wikidata_cleaned'][4][0])

# %%

s = df_b.iloc[:,0]

t = pd.get_dummies(s.apply(pd.Series).stack()).sum(level=0)
# %%

df_c = df_b.entities_instances_wikidata_cleaned.str.join('|').str.get_dummies()


# %%

print(df_c.head())
#%%

# %%
from sklearn.metrics.pairwise import pairwise_distances
jac_sim = 1 - pairwise_distances(df_c, metric = "hamming")
# optionally convert it to a DataFrame
jac_sim = pd.DataFrame(jac_sim, index=df_c.index, columns=df_c.index)
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