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
path = '../data/ed-dataset-spacy-entities-reduced.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False, converters={'spacy_entities_ids':literal_eval,'spacy_entities_labels':literal_eval,'spacy_entities_urls':literal_eval})

# %% 3

responses_entities_instances = []
responses_entities_labels = []

total_resp_entities_labels = []
total_resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

all_entities_labels_a = []
all_entities_instances_a = []

resp_list = df['spacy_entities_ids'].tolist()

for resp in resp_list:
    
    for enti in resp:
        if(enti in all_entities_instances) is False:
            all_entities_instances.append(enti)
    

# %% 4


print(df['spacy_entities_ids'][4][0])
# %%  5
 
df_orig = df.copy()
df_b = pd.DataFrame(df['spacy_entities_labels'])

# %% 6

print(df_b['spacy_entities_labels'][4][0])

# %% 7

s = df_b.iloc[:,0]

t = pd.get_dummies(s.apply(pd.Series).stack()).sum(level=0)
# %% 8

df_c = df_b.spacy_entities_labels.str.join('|').str.get_dummies()


# %% 9

print(df_c.head())


# %% 10
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
y = 0.0 + 0.0 * x + 0.00011 * np.random.standard_normal(n)
plt.hexbin(x,y)

plt.show()


jac_sim.to_csv('../data/ed-dataset-spacy-jaccard.csv',)

# pd.plotting.scatter_matrix(jac_sim, diagonal='kde')

#pd.plotting.scatter_matrix(jac_sim, alpha=0.2)
#