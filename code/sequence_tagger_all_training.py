import pandas as pd
import numpy as np
import pycrfsuite
import random
from sklearn.metrics import classification_report

def get(data: list):
    sentences = []
    sentence = []
    for element in data:
        text = str(element).lower()
        if text == 'nan':
            sentences.append(sentence)
            sentence = []
        else:
            sentence.append(text)
    return sentences

def prepare_data():
    # Load the data
    data_test = pd.read_csv("output/iob_format_test.csv")
    data_train = pd.read_csv("output/iob_format.csv")
    # Collect all IOB tags
    labels = get(list(data_train["IOB"].values))
    # Collect all sentences
    texts = get(list(data_train["Token"].values))

    c = list(zip(texts, labels))
    random.shuffle(c)
    X_train, y_train = zip(*c)
    train(X_train, y_train)

    X_test = get(list(data_test["Token"].values))
    y_test = get(list(data_test["IOB"].values))

    test(X_test, y_test)

def train(X_train, y_train):
    trainer = pycrfsuite.Trainer()
    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    # Set the parameters of the model
    trainer.set_params({'max_iterations': 125, 'feature.possible_transitions': True})
    trainer.train('output/crf.model')

def test(X_test, y_test):
    tagger = pycrfsuite.Tagger()
    tagger.open('output/crf.model')
    y_pred = [tagger.tag(xseq) for xseq in X_test]
    evaluate(y_pred, y_test)

def evaluate(y_pred, y_test):
    # Maps each label to a distinct integer
    label2int = {'b': 1, 'i': 2, 'o': 3}
    # Convert the sequences of tags into a 1-dimensional array
    predictions = np.array([label2int[tag] for sentence in y_pred for tag in sentence])
    truths = np.array([label2int[tag] for sentence in y_test for tag in sentence])
    print(classification_report(truths, predictions,target_names=["b", "i", 'o']))
