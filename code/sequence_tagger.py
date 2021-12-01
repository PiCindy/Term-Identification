import pandas as pd
import numpy as np
import pycrfsuite
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

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

def prepare_data(is_test: bool):
    # Load the data
    if is_test:
        data = pd.read_csv("output/iob_format_test.csv")
        print('Test')
    else:
        data = pd.read_csv("output/iob_format.csv")
        print('Train')
    # Collect all IOB tags
    labels = get(list(data["IOB"].values))
    # Collect all sentences
    texts = get(list(data["Token"].values))
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=36)
    #train(X_train, y_train)
    if is_test:
        test(texts, labels)
    else:
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
