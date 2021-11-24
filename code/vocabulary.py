import json

with open('output/vocabulary.json', 'r') as f:
    full_voc = json.load(f)

small_voc = {}
i=0
for key, value in full_voc.items():
    small_voc[key] = value
    i+=1
    if i==500:
        break

with open('output/500_voc.json', 'w') as f:
    json.dump(small_voc, f)
