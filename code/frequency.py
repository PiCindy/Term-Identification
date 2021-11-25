import json

frequencies = {}

with open('output/candidates.txt', 'r') as f:
    i=0
    for line in f.readlines():
        candidate = line
        frequencies[candidate] = frequencies.get(candidate, 0) + 1
        i+=1
        if i==500:
            break

sorted_freq = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1])[::-1]}
with open('output/vocabulary.json', 'w') as f:
    json.dump(sorted_freq, f)
