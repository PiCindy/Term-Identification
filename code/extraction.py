import spacy

nlp = spacy.load("en_core_web_sm")
#txt = 'Hello my name is Cindy and you? My name is Justine.'
#doc = nlp(txt)

vocabulary = set()
for file in glob.glob('articles/txt/*'):
    with open(file, 'r') as f:
        doc = nlp(f.read())
    for spacy_token in doc:
        token = spacy_token.text.lower()
        if not spacy_token.is_stop and token not in vocabulary:
            vocabulary.add(token)
print(vocabulary)
