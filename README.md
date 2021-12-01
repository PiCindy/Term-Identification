# Term-Identification
Term identification system for the domain of NLP: Speaker diarization
Created by Justine Diliberto and Cindy Pereira

### To run:
`python3 code/main.py` from main directory

### Folder `code`:
- pdftotxt.py: Convert PDF files into TXT files
- preprocessing.py: Create a TXT file with the tokens and POS of all the files
- extraction.py: Create a TXT file with all the term candidates
- sort_terms.py: Sort the terms by length (3-words terms, then 2-words terms, then 1-word terms)
- iob_tagging.py: Tag the terms with IOB
