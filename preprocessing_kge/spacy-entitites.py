# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 08:52:50 2021

@author: MICROSOFT
"""

import requests
import json
import pandas as pd
import csv
import time
import re

def clean_string(string):
        """
        Tokenization/string cleaning for all datasets except for SST.
        Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
        """
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " \( ", string)
        string = re.sub(r"\)", " \) ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r"http\S+", "", string)
        string = re.sub(r"https\S+", "", string)
        string = re.sub(r"www.\S+", "", string)
        string = re.sub("[^a-z0-9]"," ", string)
        
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        string = emoji_pattern.sub(r'', string)
        
        return string.strip().lower() 

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-lists-cleaned.csv', sep=';',index_col=0,error_bad_lines=False)

tw_list = df['text_orig'].tolist()

#%%
import spacy  # version 3.0.6'

# initialize language model
nlp = spacy.load("en_core_web_md")

# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)

# doc = nlp("I watched the Pirates of the Caribbean last silvester")




new_list_ids = [1143151,108760853,108761216,2135807,2303219]
new_list_labels = ['Pro-ana','fatspo','Meanspo','Recovery approach','binge eating']
new_list_keywords = [['proana', 'pro-ana', 'promia', 'pro-mia', 'thinspo', 'thinsp0', 'thinspiration', 'proanatwt', 'proanatweet'],
					['fatsp0', 'fatspo'],
					['Meanspo', 'Meansp0', 'meanspo','meansp0','meanspiration'],
					['prorecovery','edrecovery','anorexiarecovery'],
					['bingeeating', 'Binge Eating','bingeeatingdisorder']
			]

change_list_ids_orig = [113,283992,865,8085241,56290618,79784,1747696]
change_list_labels_orig = ['Binge','ed','Taiwan','Inge','Ana','Friends','Mia']

change_list_ids_dest = [2303219,373822,918,2303219,254327,17297777,1143151]
change_list_labels_dest = ['binge eating','eating disorder','Twitter','binge eating','anorexia','friend','Pro-ana']

remove_list_ids = [191118,33111,25272,1321647,9747,9884,9852,9973,170420,9739,9964,9751,9773,9765,1151190,199,237683]
remove_list_labels = ['tonne','Corsican','ampere','Sanga-Sanga Airport','U','D','R','Y','Nintendo Entertainment Analysis & Development','G','W','Z','J','F','Ci','1','aceme']

all_entities_ids = []
all_entities_labels = []
all_entities_urls = []

resp_entities_labels = []
resp_entities_ids = []
resp_entities_urls = []




for idx, tw in enumerate(tw_list):
    entities_ids = []
    entities_labels = []
    entities_urls = []
    tw = clean_string(tw)
    tw_list[idx] = tw
    
    for idx, kw_l in enumerate(new_list_keywords):
        for kw in kw_l:
            if(kw in  tw.lower()):
                eid = new_list_ids[idx]
                elabel = new_list_labels[idx]
                eurl = 'https://www.wikidata.org/wiki/Q'+str(new_list_ids[idx])
                resp_entities_ids.append(eid)
                resp_entities_labels.append(elabel)
                resp_entities_urls.append(eurl)
                entities_ids.append(eid)
                entities_labels.append(elabel)
                entities_urls.append(eurl)
    
    doc = nlp(tw)
    all_linked_entities = doc._.linkedEntities
    # iterates over sentences and prints linked entities
    for sent in doc.sents:
        for entity in sent._.linkedEntities:
            eid = entity.get_id()
            elabel = entity.get_label()
            eurl = entity.get_url()
            if(eid in change_list_ids_orig):
                eid = change_list_ids_dest[change_list_ids_orig.index(eid)]
                elabel = change_list_labels_dest[change_list_ids_dest.index(eid)]
                eurl = 'https://www.wikidata.org/wiki/Q'+str(eid)
            if(eid in remove_list_ids) is False:
                resp_entities_ids.append(eid)
                resp_entities_labels.append(elabel)
                resp_entities_urls.append(eurl)
                entities_ids.append(eid)
                entities_labels.append(elabel)
                entities_urls.append(eurl)
    all_entities_ids.append(entities_ids)
    all_entities_labels.append(entities_labels)
    all_entities_urls.append(entities_urls)



# %%

df['spacy_entities_ids'] = all_entities_ids
df['spacy_entities_urls'] = all_entities_urls
df['spacy_entities_labels'] = all_entities_labels

df.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-spacy-entities.csv', sep=';')


# %%

resp_entities_id_uniq = []
resp_entities_size = []
resp_entities_labels_uniq = []
resp_entities_urls_uniq = []

for idx, eid in enumerate(resp_entities_ids):
    if (eid in resp_entities_id_uniq) is False:
        resp_entities_labels_uniq.append(resp_entities_labels[idx])
        resp_entities_id_uniq.append(resp_entities_ids[idx])
        resp_entities_urls_uniq.append(resp_entities_urls[idx])
        resp_entities_size.append(1)
    else:
        index = resp_entities_id_uniq.index(eid)
        resp_entities_size[index] += 1
        

dfLabels = pd.DataFrame({'labels':resp_entities_labels_uniq,'count':resp_entities_size,'entity':resp_entities_id_uniq,'url':resp_entities_urls_uniq})

dfLabels.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-spacy-entities-count.csv', sep=';')




