import glob
import json
import spacy
from spacy.matcher import Matcher

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def sort_by_freq(candidates: dict):
    '''
    Selects the 500 most frequent term candidates
    '''
    sorted_candidates = {k: v for k, v in sorted(candidates.items(), key=lambda item: item[1])[::-1]}
    five_hundred_voc = {}
    i=0
    for candidate, frequence in sorted_candidates.items():
        five_hundred_voc[candidate] = frequence
        i+=1
        if i==500:
            break
    with open('output/vocabulary.json', 'w') as f:
        json.dump(five_hundred_voc, f)


def candidates_of_file(text: str):
    '''
    Extracts the candidates for terms from a text and write them in a file
    input: a text (string)
    '''
    if len(text) > 1000000:
        text = text[:999999]
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    patterns = [[{'POS':'NOUN'}],
               [{'POS':'VERB'}, {'POS':'NOUN'}],
               [{'POS':'ADJ'}, {'POS':'NOUN'}],
               [{"POS": "NOUN"}, {"POS": "NOUN"}],
               [{'POS':'NOUN'}, {'POS':'NOUN'}, {'POS':'NOUN'}]]
    matcher.add("Found", patterns)
    matches = matcher(doc)
    candidates = {}
    with open("output/candidates.txt", 'a') as f:
        for element in matches:
            _, beg, end = element
            candidate = str(doc[beg:end])+'\n'
            f.write(candidate)
            candidates[candidate] = candidates.get(candidate, 0) + 1
    return candidates

def candidates(path):
    # Erase the candidate file if existing
    open("output/candidates.txt", 'w').close()
    for file in glob.glob(path):
        with open(file, 'r') as f:
            text = f.read().lower()
            text = text.replace('\n', ' ')
            candidates = candidates_of_file(text)
            sort_by_freq(candidates)
