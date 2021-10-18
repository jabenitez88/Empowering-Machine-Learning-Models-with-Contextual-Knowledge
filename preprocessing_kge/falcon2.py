import requests
import json
import pandas as pd
import csv
import time
import re

# Defining a method to clean string removing emojis and other characters

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
        
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        string = emoji_pattern.sub(r'', string)
        
        return string.strip().lower() 

# %% 1. Reading CSV with tweets 


df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset.csv', sep=';',error_bad_lines=False)
print(df.head)

tw_list = df['text_orig'].tolist()

# %% 
# 2. Defining endpoint to retrieve entities of tweets using FALCON (DBPedia) or FALCON 2.0 (Wikidata) 


url = "https://labs.tib.eu/falcon/falcon2/api?mode=long"
headers = {
  'Content-Type': 'application/json'
}


resp_list = [] # list to save all json responses to requests to FALCON or FALCON 2.0
start_time = time.time()

# 3. Retrieving resources from Wikidata or DBPedia for each tweet

tw_count = 0
for tw in tw_list:
    tw = clean_string(tw)
    tw_list[tw_count] = tw
    payload = json.dumps({"text":tw})
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    resp_list.append(response.text)

end_time = time.time()
final_time = end_time - start_time
final_time_h = final_time/3600

print("--- %s seconds ---" % (final_time))
print("--- %s hours ---" % (final_time_h))


df['falcon2_responses'] = resp_list


# %% 
# 4. Saving new dataset with all json responses for each tweet


df.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2.csv', sep=';')
print(df)

#response2 = response.json();
#print(response2['entities_wikidata'])


# %% 
# 5. Showing the first entity found in each tweet.

for resp in resp_list:
    try:
        result=json.loads(resp)
        if len(result['entities_wikidata']) > 0:
            print(result['entities_wikidata'][0][0])
    except ValueError:
        print("No entities found")

    

# %% 
# 6. Once we retrieved entities, we load in df all data

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2.csv', sep=',',header=None, names=['id','id_tweet','url_tweet','text_orig','ED_Patient','ProED','informative','scientific','hashtags','falcon2_responses'
],error_bad_lines=False)


print(df.head)
print(df.text_orig)

tw_list = df['text_orig'].tolist()
resp_list = df['falcon2_responses'].tolist()


#%%

# 7. Trying to retrieve failed responses of FALCON 2.0

resp_id = 0
tot = 0
for idx, resp in enumerate(resp_list):
    if(len(resp) == 290):
        print(idx,' ',tw_list[resp_id])
        tw_list[idx] = clean_string(tw_list[idx])
        tot+=1
        tw = tw_list[resp_id]
        payload = json.dumps({"text":tw})
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        resp_list[idx] = response.text

    resp_id+=1
    
print(tot)

df['falcon2_responses'] = resp_list
df.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2b.csv',sep=';')



# %% 

responses_entities_instances = []
responses_entities_labels = []

resp_entities_labels = []
resp_entities_instances = []

all_entities_labels = []
all_entities_instances = []

all_entities_labels_a = []
all_entities_instances_a = []

for resp in resp_list:
    #resp_entities_labels = []
    #resp_entities_instances = []
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
                    all_entities_instances_a.append(entity[0])
                    all_entities_labels_a.append(entity[1])
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

print(resp_entities_labels)

# %%

resp_entities_1 = []
resp_entities_size = []
resp_entities_e = []

for idx, label in enumerate(resp_entities_labels):
    if (label in resp_entities_1) is False:
        resp_entities_1.append(label)
        resp_entities_e.append(resp_entities_instances[idx])
        resp_entities_size.append(1)
    else:
        index = resp_entities_1.index(label)
        resp_entities_size[index] += 1
        

dfLabels = pd.DataFrame({'labels':resp_entities_1,'count':resp_entities_size,'entity':resp_entities_e})

# %%

print(dfLabels[dfLabels['count']>1])



# %% 
# Using wikidata to retrieve superclasses of entitites retrieved.
# P31? is "instance of"
# P279? is "subclass of"
from qwikidata.sparql  import return_sparql_query_results

query_string = """
        SELECT DISTINCT ?item ?itemLabel
WHERE {
{ <http://www.wikidata.org/entity/Q444835> wdt:P31? ?item . } 
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} 
        """
print(query_string)
res = return_sparql_query_results(query_string)
for row in res["results"]["bindings"]:
   print(row["itemLabel"]["value"])
   
   
# %%

 
qs1 = """
SELECT DISTINCT ?item ?itemLabel
WHERE {
       {
       """
qs2 = """ wdt:P31? ?item . } 
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} 
        """

all_ent_subcl_labels = []
all_ent_subcl_ins = []
all_ent_ins = []
all_ent_labels = []

error_retrieving_class = []

conta=0
for idx, entity in enumerate(all_entities_instances_a):
    
    #print(idx, entity)
    query_string = qs1 + entity + qs2
    print(idx,entity)
    try:
        res = return_sparql_query_results(query_string)
        if(idx%4==0):
            time.sleep(12)
        if(res["results"] is not False):
            for row in res["results"]["bindings"]:
                all_ent_subcl_labels.append(row["itemLabel"]["value"])
                all_ent_subcl_ins.append(row["item"]["value"])
                all_ent_ins.append(entity)
                all_ent_labels.append(all_entities_labels[idx])
                if(conta==0):
                    print(row["item"]["value"])
                    conta+=1
    except:
        error_retrieving_class.append(entity)
        print('error',idx,entity)

   
# %% 



for idx, entity in enumerate(error_retrieving_class): 
    #print(idx, entity)
    query_string = qs1 + entity + qs2
    print(idx,entity)
    try:
        res = return_sparql_query_results(query_string)
        if(idx%4==0):
            time.sleep(12)
        if(res["results"] is not False):
            for row in res["results"]["bindings"]:
                all_ent_subcl_labels.append(row["itemLabel"]["value"])
                all_ent_subcl_ins.append(row["item"]["value"])
                all_ent_ins.append(entity)
                all_ent_labels.append(all_entities_labels[idx])
                if(conta==0):
                    print(row["item"]["value"])
                    conta+=1
    except:
        #error_retrieving_class.append(entity)
        print('error',idx,entity)

# %%

df_classes = pd.DataFrame({'Entities':all_ent_ins,'Enti_labels':all_ent_labels,'Classes':all_ent_subcl_ins,'Class_labels':all_ent_subcl_labels})
df_classes 

# %%

df_classes.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-classes-entities.csv',sep=';')

# %% 

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-classes-entities.csv', sep=';',error_bad_lines=False)
print(df.head)
df['Entities'] = df['Entities'].map(lambda x: x.lstrip('<').rstrip('>'))

df_1 = df.query("Entities != Classes")

df_1

df_1.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcon2-classes-entities.csv',sep=';')


