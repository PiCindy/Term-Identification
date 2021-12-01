import spacy
import glob
import pandas as pd
import sequence_tagger

def iob_formatting(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens_iob = []
    for token in doc:
        tokens_iob.append(token.text)
    return tokens_iob

def iob_tagging(tokens: list, terms: list):
    iob = []
    i, j, k = 0, 1, 2
    while i < len(tokens):
        token = str(tokens[i])
        found = False
        if token == 'nan':
            iob.append('')
            found = True
            i+=1
            j+=1
            k+=1
        for term in terms:
            st = term.strip().split(' ')
            if len(st) == 1:
                if token == st[0]:
                    iob.append('b')
                    found = True
                    i+=1
                    j+=1
                    k+=1
                    break
            elif j < len(tokens) and len(st) == 2:
                second_token = tokens[j]
                if token == st[0] and second_token == st[1]:
                    iob.append('b')
                    iob.append('i')
                    i+=2
                    j+=2
                    k+=2
                    found = True
                    break
            elif k < len(tokens) and len(st) == 3:
                second_token = tokens[j]
                third_token = tokens[k]
                if token == st[0] and second_token == st[1] and third_token == st[2]:
                    iob.append('b')
                    iob.append('i')
                    iob.append('i')
                    i+=3
                    j+=3
                    k+=3
                    found = True
                    break
        if not found:
            iob.append('o')
            i+=1
            j+=1
            k+=1
    return iob

def tag_files(test:bool):
    # Load the data
    if test:
        data = pd.read_csv("output/ground_truth_iob.csv")
        iob_path = "output/iob_format_test.csv"
    else:
        data = pd.read_csv("output/iob_format.csv")
        iob_path = "output/iob_format.csv"
    tokens = list(data["Token"].values)
    pos = list(data["POS"].values)
    terms = []
    with open('output/sorted_terms.txt', 'r') as f:
        for line in f.readlines():
            terms.append(line)
    iob = iob_tagging(tokens, terms)
    data = {'Token':tokens, "POS":pos, "IOB":iob}
    df = pd.DataFrame(data=data)
    df.to_csv(iob_path, index=False)
    return iob
