#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:40:20 2021

@author: jabenitez
"""

import requests
import json
import pandas as pd
import csv
import time
import re
import os

from pathlib import Path


path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-entities.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False)
print(df.head)

# ed-spacy-entities-count-reduced.csv
# ed-spacy-entities-count-reduced2.csv
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-spacy-entities-count-reduced2.csv'
df_entities = pd.read_csv(path, sep=';',error_bad_lines=False)
print(df_entities.head)



l_entities_labels = df_entities['labels'].tolist()
l_entities_instances = df_entities['entity'].tolist()
l_entities_urls = df_entities['url'].tolist()


l_tw_entities_instances = df['spacy_entities_ids'].tolist()
l_tw_entities_labels = df['spacy_entities_labels'].tolist()
l_tw_entities_urls = df['spacy_entities_urls'].tolist()


for idx, entity in enumerate(l_tw_entities_instances):
    l_tw_entities_instances[idx] = l_tw_entities_instances[idx].replace('[','').replace(']','').replace("'",'').replace(' ','').split(',')
    l_tw_entities_labels[idx] = re.findall("'([^']*)'", l_tw_entities_labels[idx])
    l_tw_entities_urls[idx] = l_tw_entities_urls[idx].replace('[','').replace(']','').replace("'",'').replace(' ','').split(',')

    #l_tw_entities_labels[idx] = ['"{}"'.format(l_tw_entities_labels[idx]) for l_tw_entities_labels[idx] in l_tw_entities_labels[idx].split("'") if l_tw_entities_labels[idx] not in ('', ', ')]
    #l_tw_entities_labels[idx] = l_tw_entities_labels[idx].replace('[','').replace("'","").replace(']','').split(',')


l_tw_entities_instancesPre = l_tw_entities_instances
l_tw_entities_labelsPre = l_tw_entities_labels




#%%
cont = 0
cont2= 0
for idx1, tw_labels in enumerate(l_tw_entities_labels):
    #tw_labels = 
    for idx2, tw_label in enumerate(tw_labels):
        try:
            if(tw_label in l_entities_labels):
                print(cont)
                cont+=1
                idx3 = l_entities_labels.index(tw_label)
                l_tw_entities_instances[idx1][idx2] = l_entities_instances[idx3]
                l_tw_entities_urls[idx][idx2]  = l_entities_urls[idx3]
            else:
                print(cont2)
                cont2+=1
                l_tw_entities_instances[idx1][idx2] = 'Vac'
                l_tw_entities_labels[idx1][idx2] = 'Vac'
                l_tw_entities_urls[idx][idx2]  = 'Vac'
                #l_tw_entities_labels[idx1].pop(idx2)
                #l_tw_entities_instances[idx1].pop(idx2) 
        except:
            print(idx1,idx2)
            

# %%        


            
for idx1, tw_labels in enumerate(l_tw_entities_labels):
    val = 'Vac'
    l_tw_entities_labels[idx1] = list(filter(lambda x: x != val, l_tw_entities_labels[idx1]))


for idx2, tw_entities in enumerate(l_tw_entities_instances):
    val = 'Vac'
    l_tw_entities_instances[idx2] = [i for i in l_tw_entities_instances[idx2] if i != val]

for idx3, tw_urls in enumerate(l_tw_entities_urls):
    val = 'Vac'
    l_tw_entities_urls[idx3] = [i for i in l_tw_entities_urls[idx3] if i != val]
# %%

print(cont)
print(cont2)
#%%


df['spacy_entities_ids'] = l_tw_entities_instances
df['spacy_entities_labels'] = l_tw_entities_labels
df['spacy_entities_urls']  = l_tw_entities_urls



path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-entities-reduced2.csv'

df.to_csv(path,sep=';')
# %% 

# l = l_tw_entities_labels[1998]
# l2 = l_tw_entities_instances[1998]

# print(l_tw_entities_instances[1998])

# 

print(df_entities['entity'].unique())

df_unique_entities = pd.DataFrame({'Unique_Entitites':df_entities['entity'].unique()})
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-unique-entities2.csv'

df_unique_entities.to_csv(path,sep=';')
