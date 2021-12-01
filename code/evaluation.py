import pandas as pd
import numpy as np
import sequence_tagger
from sklearn.metrics import classification_report

def evaluate(y_pred=None):
    data_truth = pd.read_csv("output/ground_truth_iob.csv")
    y_truth = sequence_tagger.get(list(data_truth["IOB"].values))
    if y_pred == None:
        data_test = pd.read_csv('output/iob_format_test.csv')
        y_pred = sequence_tagger.get(list(data_test["IOB"].values))
    # Maps each label to a distinct integer
    label2int = {'b': 1, 'i': 2, 'o': 3}
    # Convert the sequences of tags into a 1-dimensional array
    predictions = np.array([label2int[tag] for sentence in y_pred for tag in sentence])
    truths = np.array([label2int[tag] for sentence in y_truth for tag in sentence])
    print(classification_report(truths, predictions, target_names=["b", "i", "o"]))
