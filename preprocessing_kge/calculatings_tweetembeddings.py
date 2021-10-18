# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:03:47 2021

@author: MICROSOFT
"""

# %%
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

import sys
sys.path.append('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\libraries')
import data_io, params, SIF_embedding

# %% Load df

path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-embeddings-md4.csv'
df = pd.read_csv(path, sep=';',error_bad_lines=False,
                 converters={
                     'falcon_spacy_labels':literal_eval,
                     'falcon_spacy_entities':literal_eval,
                             #'falcon_spacy_embeddingsmd4_mw50_RW':literal_eval,
                            #'falcon_spacy_embeddingsmd2_mw100_RW':literal_eval,
                            'falcon_spacy_embeddingsmd4_mw50_RW':literal_eval})

path = 'G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-entities-uniques-embeddings-md4.csv'
dfEmbeddings = pd.read_csv(path, sep=';',error_bad_lines=False,converters=
                           {
                            #'embeddings-md2_mw50_RW':literal_eval,
                            #'embeddings-md2_mw100_RW':literal_eval,
                            'embeddings-md4_mw50_RW':literal_eval})

# %% Frequencies of entitites in corpus

sentences = df['falcon_spacy_entities']
sentences_labels = df['falcon_spacy_labels']

entities_id = []
entities_count = []
labels_id = []

vocab = dfEmbeddings['labels-md4_mw50_RW']


for idx1, sentence in enumerate(sentences):
    for idx2, entity in enumerate(sentence):
        if((entity is not None) and (entity is not '')):
            if(entity in entities_id):
                idx_entity = entities_id.index(entity)
                entities_count[idx_entity] += 1
            else:
                entities_id.append(entity)
                entities_count.append(1)
                if(idx2 < len(sentences_labels[idx1])):
                    labels_id.append(sentences_labels[idx1][idx2])
                else:
                    labels_id.append(entity)
                

vocab_freq = pd.DataFrame({'label':entities_id,'freq':entities_count})


vocab = entities_id
embed = []
embed.append(dfEmbeddings['embeddings-md4_mw50_RW'])
#embed.append(dfEmbeddings['embeddings-md2_mw100_RW'])
#embed.append(dfEmbeddings['embeddings-md2_mw200_RW'])

sentences_l = df['falcon_spacy_labels']
sentences = []
for idx, sentence in enumerate(sentences_l):
    sentence = ' '.join(sentence)
    if (sentence is ''):
        sentence = 'N'
    sentences.append(sentence)
print(sum(entities_count))

# %% SIF

'''
import numpy as np
# input
wordfile = 'G:/Mi unidad/HANNOVER 2021/TRABAJO/Ahmad/SCRIPTS/data/test.txt' # word vector file, can be downloaded from GloVe website
weightfile = 'G:/Mi unidad/HANNOVER 2021/TRABAJO/Ahmad/SCRIPTS/auxiliary_data/enwiki_vocab_min200.txt' # each line is a word and its frequency
weightpara = 3e-5 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 0 # number of principal components to remove in SIF weighting scheme

words = {}
We_l = []

for idx, word in enumerate(vocab):
    words[word] = idx
    We_l.append(embed[1][idx])
    
We = np.array(We_l)



# load word weights
wordlist = entities_id
weightlist = entities_count
word2weight = data_io.getWordWeightList(wordlist, weightlist, weightpara) # word2weight['str'] is the weight for the word 'str'



sentences = ['this is an example sentence', 'this is another sentence that is slightly longer']
(words, We) = data_io.getWordmap(wordfile)
word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'

weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word
# load sentences
x, m = data_io.sentences2idx(sentences, words) # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
w = data_io.seq2weight(x, m, weight4ind) # get word weights

# set parameters
#params = params.params()
#params.rmpc = rmpc
#params = s
params = 0
# get SIF embedding
embedding = SIF_embedding.SIF_embedding(We, x, w, params) # embedding[i,:] is the embedding for sentence i
'''

# %% Jabe embeddings calc

sent_embeddings_list_1 = []
sent_embeddings_list_2 = []

embeddings_list_1 = df['falcon_spacy_embeddingsmd4_mw50_RW'].tolist()
#embeddings_list_2 = df['falcon_spacy_embeddingsmd2_mw100_RW'].tolist()






import numpy as np

# loco = np.array(embeddings_list_1[0][0]) + np.array(embeddings_list_1[0][1])/2

sent_embedding_list_1_mean = []

for sentence in embeddings_list_1:
    sent_embedding = np.zeros(100)
    for embedding in sentence:
        sent_embedding += np.array(embedding)
    sent_embedding /= len(sentence)
    
    sent_embeddings_list_1.append(list(sent_embedding))
    sent_embedding_list_1_mean.append(sent_embedding.mean())
    
        

sent_embedding_list_1_mean = pd.Series(sent_embedding_list_1_mean).fillna(0).tolist()
sent_embedding_list_1_mean2 =  pd.Series(sent_embedding_list_1_mean).fillna(0).tolist()

print(1 + sent_embedding_list_1_mean[0] - (sent_embedding_list_1_mean2[0]))

'''
sent_embedding_list_2_mean = []

for sentence in embeddings_list_2:
    sent_embedding = np.zeros(100)
    for embedding in sentence:
        sent_embedding += np.array(embedding)
    sent_embedding /= len(sentence)
    sent_embeddings_list_2.append(sent_embedding)
    sent_embedding_list_2_mean.append(sent_embedding.mean())
    
        

sent_embedding_list_2_mean = pd.Series(sent_embedding_list_2_mean).fillna(0).tolist()
sent_embedding_list_2_mean2 =  pd.Series(sent_embedding_list_2_mean).fillna(0).tolist()
'''

# %%

df['sent_embedding_1'] = sent_embeddings_list_1
#df['sent_embedding_2'] = sent_embeddings_list_2

df.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-embeddings-sentence-md4.csv',sep=';')

#%%

#Declaring an empty 1D array.
embeddings_similarity_matrix = []
#Declaring an empty 1D array.
b = []
#Initialize the column.

#Append the column to each row.
for i in range(0, 2000):
    b = []
    for j in range(0, 2000):
        b.append(float(0))
    embeddings_similarity_matrix.append(b)
  
    
# %%
print(1 - sent_embedding_list_1_mean[0] - sent_embedding_list_1_mean[1])
print(1 - sent_embedding_list_1_mean[0] - sent_embedding_list_1_mean[2])
print(1 - sent_embedding_list_1_mean[0] - sent_embedding_list_1_mean[3])

#matrix = np.array(0).reshape(2000,2000)

import random


for idx1, fila in enumerate(sent_embedding_list_1_mean):
    for idx2, colu in enumerate(sent_embedding_list_1_mean2):
        if(fila>colu):
            embeddings_similarity_matrix[idx1][idx2] = ((1.0)-(fila+colu))*random.uniform(1,1)
        elif(fila==colu):
            embeddings_similarity_matrix[idx1][idx2] = 1.0
        else:
            embeddings_similarity_matrix[idx1][idx2] = ((1.0)-(colu-fila))*random.uniform(1,1)
        if(idx1 <10):
            if(idx2==idx1):
                print('f',fila, colu,(fila-colu-1*-1))
#%%


print(sent_embeddings_list_1[2].mean())


# %% JACCARD SEQUENCE
df_b = pd.DataFrame(embeddings_similarity_matrix)

df_b.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon_spacy2-embeddings-similarity_matrix_2.csv',sep=';')
