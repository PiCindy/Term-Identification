import spacy
import glob
import pandas as pd


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
        token = tokens[i]
        found = False
        if token == '':
            iob.append('')
            found = True
            i+=1
            j+=1
            k+=1
        for term in terms:
            st = term.strip().split(' ')
            if len(st) == 1:
                if token == st[0]:
                    iob.append('B')
                    found = True
                    i+=1
                    j+=1
                    k+=1
                    break
            elif j < len(tokens) and len(st) == 2:
                second_token = tokens[j]
                if token == st[0] and second_token == st[1]:
                    iob.append('B')
                    iob.append('I')
                    i+=2
                    j+=2
                    k+=2
                    found = True
                    break
            elif k < len(tokens) and len(st) == 3:
                second_token = tokens[j]
                third_token = tokens[k]
                if token == st[0] and second_token == st[1] and third_token == st[2]:
                    iob.append('B')
                    iob.append('I')
                    iob.append('I')
                    i+=3
                    j+=3
                    k+=3
                    found = True
                    break
        if not found:
            iob.append('O')
            i+=1
            j+=1
            k+=1
    return iob


def tag_files(test: bool):
    if test:
        path = 'output/tokens_pos_test.txt'
        iob_path = "output/iob_format_test.csv"
    else:
        path = 'output/tokens_pos.txt'
        iob_path = "output/iob_format.csv"
    with open(iob_path, 'r+') as f:
        f.truncate(0)
    terms, tokens, pos = [], [], []
    with open('output/sorted_terms.txt', 'r') as f:
        for line in f.readlines():
            terms.append(line)
    with open(path, 'r') as f:
        for line in f.readlines():
            sl = line.split('\t')
            if len(sl) == 1:
                tokens.append('')
                pos.append('')
            else:
                tokens.append(sl[0].strip('\n'))
                pos.append(sl[1].strip('\n'))
    iob = iob_tagging(tokens, terms)
    data = {'Token':tokens, "POS":pos, "IOB":iob}
    df = pd.DataFrame(data=data)
    df.to_csv(iob_path, index=False)
