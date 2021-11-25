import spacy
import glob

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

open("output/tokens_pos.txt", 'w').close()
for file in glob.glob('articles/txt/*'):
    print(file)
    tokens_pos = []
    with open(file, 'r') as f:
        text = f.read()
        text = text.replace('\n', ' ')
        tokens_pos.append(pos_tagger(text))
