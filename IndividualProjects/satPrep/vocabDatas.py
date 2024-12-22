
with open('final_data.txt','r') as f:
    raw_data = f.read()


import json

data = json.loads(raw_data)

print(data)

#data structure: a dictionary
#each key: a word
#each word corresponds to a list, containing data of definitions
#each definition (list) contains two elements, the first one is the word type, the second one is the definition

