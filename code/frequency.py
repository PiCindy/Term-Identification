import json

frequencies = {}

with open('output/candidates.txt', 'r') as f:
    for line in f.readlines():
        candidate = line
        frequencies[candidate] = frequencies.get(candidate, 0) + 1

sorted_freq = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1])[::-1]}

five_hundred_voc = {}
i=0
for key, value in sorted_freq.items():
    five_hundred_voc[key] = value
    i+=1
    if i==500:
        break

with open('output/vocabulary.json', 'w') as f:
    json.dump(five_hundred_voc, f)
