import spacy
import glob

def iob_formatting(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens_iob = []
    for token in doc:
        tokens_iob.append(token.text)
    return tokens_iob

def iob_tagging(tokens: list, terms: list):
    tokens_iob = []
    i, j, k = 0, 1, 2
    while k < len(tokens):
        token = tokens[i]
        second_token = tokens[j]
        third_token = tokens[k]
        found = False
        for term in terms:
            st = term.strip().split(' ')
            if len(st) == 1:
                if token == st[0]:
                    tokens_iob.append((token, 'B'))
                    i+=1
                    j+=1
                    k+=1
                    found = True
                    break
            elif len(st) == 2:
                if token == st[0] and second_token == st[1]:
                    tokens_iob.append((token, 'B'))
                    tokens_iob.append((second_token, 'I'))
                    i+=2
                    j+=2
                    k+=2
                    found = True
                    break
            elif len(st) == 3:
                if token == st[0] and second_token == st[1] and third_token == st[2]:
                    tokens_iob.append((token, 'B'))
                    tokens_iob.append((second_token, 'I'))
                    tokens_iob.append((third_token, 'I'))
                    i+=3
                    j+=3
                    k+=3
                    found = True
                    break
        if not found:
            tokens_iob.append((token, 'O'))
            i+=1
            j+=1
            k+=1
    return tokens_iob



open("output/iob_format.txt", 'w').close()

terms = []
with open('output/sorted_terms.txt', 'r') as f:
    for line in f.readlines():
        terms.append(line)

docs = []
for file in glob.glob('articles/txt/*'):
    print(file)
    with open(file, 'r') as f:
        text = f.read().lower()
        text = text.replace('\n', ' ')
        docs.append(iob_formatting(text))

tokens_iob = []
for doc in docs:
    tokens_iob.append(iob_tagging(doc, terms))

with open('output/iob_format.txt', 'w') as f:
    for doc in tokens_iob:
        for token, iob in doc:
            line = f'{token}\t{iob}\n'
            f.write(line)
        f.write('\n')
