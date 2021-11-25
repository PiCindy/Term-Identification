import spacy
import glob
from spacy.matcher import Matcher


nlp = spacy.load("en_core_web_sm")

def pos_tagger(text: str):
    ''' Preprocess a text using spaCy part-of-speech tagger
    Create file of form "token part-of-speech" one per line
    input: the text we want to preprocess (string)
    output: a list with tuples (token lemma part-of-speech)'''
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens_pos = []
    with open("output/tokens_pos.txt", 'a') as f:
        for token in doc:
            line = f'{token.text}\t{token.lemma_}\t{token.pos_}\n'
            f.write(line)
            tokens_pos.append((token.text, token.lemma_, token.pos))
    return tokens_pos

def candidates_extraction(text: str):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    patterns = [[{'POS':'NOUN'}],
               [{'POS':'VERB'}, {'POS':'NOUN'}],
               [{'POS':'ADJ'}, {'POS':'NOUN'}],
               [{"POS": "NOUN"}, {"POS": "NOUN"}],
               [{'POS':'NOUN'}, {'POS':'NOUN'}, {'POS':'NOUN'}]]
    matcher.add("Found", patterns)
    matches = matcher(doc)
    with open("output/candidates.txt", 'a') as f:
        for element in matches:
            _, beg, end = element
            line = str(doc[beg:end])+'\n'
            f.write(line)

open("output/candidates.txt", 'w').close()
for file in glob.glob('articles/txt/*'):
    print(file)
    tokens_pos = []
    with open(file, 'r') as f:
        text = f.read()
        text = text.replace('\n', ' ')
        candidates_extraction(text)
