import spacy
import glob
import nltk

def pos_tagger(sentences: list, pos_file):
    ''' Preprocess a text using spaCy part-of-speech tagger
    Create file of form "token part-of-speech" one per line
    input: the text we want to preprocess (list)'''
    nlp = spacy.load("en_core_web_sm")
    for sentence in sentences:
        doc = nlp(sentence)
        with open(pos_file, 'a') as f:
            for token in doc:
                if ',' not in token.text and token.text != 'null' and token.text != 'nan':
                    line = f'{token.text}\t{token.pos_}\n'
                    f.write(line)
            f.write('\n')

def preprocess(test: bool):
    '''
    Preprocess all files corresponding to the path
    input: True if we are in test setting
    '''
    if test:
        pos_file = "output/tokens_pos_test.txt"
        path = r'articles/txt/test/*'
    else:
        pos_file = "output/tokens_pos.txt"
        path = r'articles/txt/train/*'

    open(pos_file, 'w').close()

    for file in glob.glob(path):
        with open(file, 'r') as f:
            text = f.read()
            text = text.replace('\n', ' ')
            sentences = nltk.sent_tokenize(text)
            lowered_sentences = [sentence.lower() for sentence in sentences]
            pos_tagger(lowered_sentences, pos_file)
