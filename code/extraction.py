import spacy

nlp = spacy.load("en_core_web_sm")

# create set
vocabulary = set()		
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
        if not spacy_token.is_stop and token not in vocabulary: 	
            vocabulary.add(token)

print(len(vocabulary))
