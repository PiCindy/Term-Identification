terms = []
with open('output/terms.txt', 'r') as f:
    for line in f.readlines():
        terms.append(line)

sorted_terms = []
for term in terms:
    splitted = term.split(' ')
    if len(splitted) == 3:
        terms.remove(term)
        sorted_terms.append(term)
for term in terms:
    splitted = term.split(' ')
    if len(splitted) == 2:
        terms.remove(term)
        sorted_terms.append(term)
for term in terms:
    splitted = term.split(' ')
    if len(splitted) == 1:
        terms.remove(term)
        sorted_terms.append(term)

with open('output/sorted_terms.txt', 'w') as f:
    for term in sorted_terms:
        f.write(term)
