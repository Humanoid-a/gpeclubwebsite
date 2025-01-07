with open('final_data.json', 'r') as f:
    raw_data = f.read()


import json

data = json.loads(raw_data)

print(data)

vocab_count = len(data)
set_count = 33
word_per_set = 2647 // set_count

words = list(data.keys())

import os

next_key = 0

for set_i in range(1,set_count+1):
    set_data = {}
    for _ in range(word_per_set):
        word = words[next_key]
        set_data.update({word: data[word]})
        next_key += 1
    set_file_str = json.dumps(set_data)
    with open("wordData/set{}.json".format(set_i), 'w') as f:
        f.write(set_file_str)

#data structure: a dictionary
#each key: a word
#each word corresponds to a list, containing data of definitions
#each definition (list) contains two elements, the first one is the word type, the second one is the definition

