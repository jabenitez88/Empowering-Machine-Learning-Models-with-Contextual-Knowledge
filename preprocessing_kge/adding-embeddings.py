# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 18:20:17 2021

@author: MICROSOFT
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
# %% 2
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False, converters={
    'entities_instances_wikidata_cleaned':literal_eval,
    'falcon_spacy_entities':literal_eval,
    'falcon_spacy_labels':literal_eval})

embeddings_files_names = ['md2_mw50_RW','md2_mw100_RW']
embeddings_files_names = ['md4_mw50_RW']
dfUniques = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-entities-uniques.csv',sep=';')

embeddings_l = []
entities_l = []

ds_entities_l = df['falcon_spacy_entities']
ds_labels_ = dfUniques['label'].tolist()
ds_entities_ = dfUniques['entity'].tolist()

for idx, emb_file in enumerate(embeddings_files_names):
    path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\embeddings\extract2_'+emb_file+'.json'

    f = open(path,)
    embeddings = json.load(f)
    #print(embeddings)

    embeddings_l = embeddings['embeddings']
    entities_l = embeddings['entities']
    labels_l = []
    
    for idxe, entity in enumerate(entities_l):
        idx2 = ds_entities_.index(entity)
        labels_l.append(ds_labels_[idx2])

    if(idx==0):
        dfEmbeddings = pd.DataFrame({'labels-'+embeddings_files_names[idx]:labels_l,
                                     'entities-'+embeddings_files_names[idx]:entities_l,
                                     'embeddings-'+embeddings_files_names[idx]:embeddings_l})
    else:
        dfEmbeddings['entities-'+embeddings_files_names[idx]] = entities_l
        dfEmbeddings['embeddings-'+embeddings_files_names[idx]] = embeddings_l
        
    ds_embeddings_l = []

    for idx1, tw_entities_l in enumerate(ds_entities_l):
        tw_embeddings_l = []
        for idx2, entity in enumerate(tw_entities_l):
            if(entity in entities_l):
                idx_entity = entities_l.index(entity)
                tw_embeddings_l.append(embeddings_l[idx_entity])
        ds_embeddings_l.append(tw_embeddings_l)
    
    df['falcon_spacy_embeddings'+embeddings_files_names[idx]] = ds_embeddings_l
    
path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-entities-uniques-embeddings-md4.csv'
dfEmbeddings.to_csv(path,sep=';')



path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-embeddings-md4.csv'
df.to_csv(path,sep=';')






