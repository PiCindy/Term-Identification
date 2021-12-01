import pdftotxt
import preprocessing
import extraction
import sort_terms
import iob_tagging
import sequence_tagger

import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# To convert all train data into txt, uncomment the following line
#pdftotxt.convert(r'articles/pdf/train/*')
# To preprocess all train data, uncomment the following line
#preprocessing.preprocess(False)
# To extract the term candidates for all train data, uncomment the following line
#extraction.candidates(r'articles/txt/train/*')
# To sort the terms by length, uncomment the following line
#sort_terms.sort()
# To tag the train data with IOB, uncomment the following line
#iob_tagging.tag_files(False)
# To re-train the model, uncomment the line 27 in sequence_tagger.py

# To convert all test data into txt, uncomment the following line
#pdftotxt.convert(r'articles/pdf/test/*')
# To preprocess all train data, uncomment the following line
#preprocessing.preprocess(True)
# To tag the train data with IOB, uncomment the following line
#iob_tagging.tag_files(True)

# To re-train the model, uncomment the line 27 in sequence_tagger.py
sequence_tagger.prepare_data()
