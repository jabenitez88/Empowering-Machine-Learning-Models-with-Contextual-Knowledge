import requests
import json
import pandas as pd
import csv
import time

# %% 1
url = "https://labs.tib.eu/falcon/api?mode=long"

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset.csv', sep=';',error_bad_lines=False)
#df = pd.read_csv('data\ed-dataset.csv', sep=';',error_bad_lines=False)


print(df.head)
print(df.text_orig)

tw_list = df['text_orig'].tolist()

# %% 2

# consultas = [{"text":"who is the wife of barack obama ?"},{"text":"What is the best football team?"}]

headers = {
  'Content-Type': 'application/json'
}

resp_list = []
start_time = time.time()

for tw in tw_list:
    payload = json.dumps({"text":tw})
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    resp_list.append(response.text)

end_time = time.time()

print("--- %s seconds ---" % (end_time - start_time))

#payload = json.dumps({
#  "text": "who is the wife of barack obama ?"
# })

# %% 3

df['falcon_responses'] = resp_list

df.to_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcona.csv',sep=';')
print(df)

# %% 3b

c=0
for resp in resp_list:
    if((len(resp) == 290) or (len(resp) == 3048)):
        c+=1
print(c)
        

# %% 

import requests
import json
import pandas as pd
import csv
import time
import re

df = pd.read_csv('G:\Mi unidad\HANNOVER 2021\TRABAJO\Ahmad\SCRIPTS\data\ed-dataset-falcona.csv', sep=';',error_bad_lines=False)
resp_list = df['falcon_responses'].tolist()
tw_list = df['text_orig'].tolist()
url = "https://labs.tib.eu/falcon/api?mode=long"



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

resp_id = 0
tot = 0

start_time = time.time()

for resp in resp_list:
    contreps=0
    tamresp = len(resp) 
    while(((tamresp == 290) or (tamresp == 3048)) and contreps < 4):
        if((tamresp == 290) or (tamresp == 3048)):
            print(resp_id,' ',tw_list[resp_id])
            tw_list[resp_id] = clean_string(tw_list[resp_id])
            tw = tw_list[resp_id]
            payload = json.dumps({"text":tw})
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            resp_list[resp_id] = response.text
            resp = response.text
            tamresp = len(response.text)
            contreps+=1
        else:
            tot+=1
    resp_id+=1

end_time = time.time()

print(tot)


# %% 4

final_time = end_time - start_time
final_time_h = final_time/3600
print("--- %s hours ---" % (final_time_h))

response2 = response.json();
print(response2['entities'])

# %% 5

for resp in resp_list:
    try:
        result=json.loads(resp)
        if len(result['entities']) > 0:
            print(result['entities'][0][0])
    except ValueError:
        print("la")

    

