import pandas as pd
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

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


# Load the data
data = pd.read_csv("output/iob_format.csv")
# Collect all IOB tags
labels = get(list(data["IOB"].values))
# Maps each label to a distinct integer
label2int = {'b': 1, 'i': 2, 'o': 3}
# Convert labels to the corresponding integers
int_labels = [[label2int[label] for label in sentence] for sentence in labels]
# Collect all sentences
texts = get(list(data["Token"].values))
# Remove duplicates and lowercase the tokens
words = set([token for sentence in texts for token in sentence])
# Add an end-of-sequence tag
words.add('<eos>')
# Map each token to an integer
token2int = {word: i+1 for i, word in enumerate(words)}
# Convert tokens to the corresponding integers
int_texts = [[token2int[token.lower()] for token in sentence] for sentence in texts]

# Create the reverse dictionaries
int2label = {iden:label for label, iden in label2int.items()}
int2token = {iden:token for token, iden in token2int.items()}

print(int_texts[0])

max_len = 16
batch_size = 64
embed_size = 300
hidden_size = 128
# tensor of shape (len(ls),s_len) with values 0 (long hence integers not float)
X = torch.zeros(len(texts), max_len).long()
Y = torch.zeros(len(texts), max_len).long()
for i, l in enumerate(int_texts):
    X[i] = F.pad(input=torch.LongTensor(l[:max_len]), pad=(0,max_len-len(l[:max_len])), mode='constant', value=0)
for i, l in enumerate(int_labels):
    Y[i] = F.pad(input=torch.LongTensor(l[:max_len]), pad=(0,max_len-len(l[:max_len])), mode='constant', value=0)

X_train = X[:5000]
X_test = X[5000:]
Y_train = Y[:5000]
Y_test = Y[5000:]

from torch.utils.data import TensorDataset, DataLoader
train_set = TensorDataset(X_train, Y_train)
valid_set = TensorDataset(X_test, Y_test)

train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(valid_set, batch_size=batch_size)

pretrained_weights = torch.zeros(len(token2int), 300)
tokens = {}
with open('wiki.en.filtered.vec') as f:
    for line in f:
        line = line.strip().split(' ')
        if line[0] != '0.0':
            tokens[line[0]] = torch.FloatTensor([float(x) for x in line[1:]])
            if line[0] in token2int:
                pretrained_weights[token2int[line[0]]-1] = tokens[line[0]]


vocab_size = len(token2int)
number_classes = 4

class RNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size, padding_idx=token2int['<eos>'])
        self.embed.weight = nn.Parameter(pretrained_weights, requires_grad=False)
        self.rnn = nn.GRU(embed_size, hidden_size, bias=False, num_layers=1, bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(0.3)
        self.decision = nn.Linear(hidden_size * 2 * 1, number_classes)

    def forward(self, x):
        embed = self.embed(x)
        output, hidden = self.rnn(embed)
        return self.decision(self.dropout(output))

rnn_model = RNN()
print(rnn_model)

with torch.no_grad():
  print(rnn_model(X[:2]).size())

def fit(model, epochs):
    criterion = nn.CrossEntropyLoss()
    # add gradients to all parameters (required by pytorch for training)
    optimizer = optim.Adam(filter(lambda param: param.requires_grad, model.parameters()))
    for epoch in range(epochs):
        model.train()
        total_loss = num = 0
        for x, y in train_loader:
            optimizer.zero_grad()
            y_scores = model(x)
            loss = criterion(y_scores.view(y.size(0) * y.size(1), -1), y.view(y.size(0) * y.size(1)))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            num += len(y)

rnn_model = RNN()
fit(rnn_model, 3)

def tag_sentence(model,i):
    sentence = X_test[i]
    label = Y_test[i]
    tags  = model.predict(sentence) # tags is a tensor of size (max_len, label_size); recall that label_size=4
    predictions = np.argmax(tags, axis=1) # predictions is a tensor of size (max_len, 1)
    tag_predictions  = [int2label[val] for val in predictions]
    print(tag_predictions)

for i in range(len(X_test)):
    tag_sentence(rnn_model,i)
