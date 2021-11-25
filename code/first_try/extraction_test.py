import spacy
import glob
import json

nlp = spacy.load("en_core_web_sm")

# create set
vocabulary = {}
# iterate over files
for file in glob.glob('articles/txt/*'):
    # open each file (read mode)
    with open(file, 'r') as f:
        # using spacy model, read text with it
        doc = nlp(f.read())
    # tokenize text
    for spacy_token in doc:
        # change token into string and lowercase
        token = spacy_token.text.lower()
        # adding tokens in vocabulary (if it is not a stopword and not already in voc)
        if not spacy_token.is_stop and not spacy_token.is_punct:
            vocabulary[token] = vocabulary.get(token, 0) + 1

print(len(vocabulary.keys()))
sorted_voc = {k: v for k, v in sorted(vocabulary.items(), key=lambda item: item[1])[::-1]}

with open('output/vocabulary.json', 'w') as f:
    json.dump(sorted_voc, f)
