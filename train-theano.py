#! /usr/bin/env python

import csv
import itertools
import operator
import numpy as np
import nltk
import sys
import os
import time

import distance
from datetime import datetime
from utils import *
from rnn_theano import RNNTheano

_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '1000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '500')) # size it up to 1000 is an idea
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '50'))
_MODEL_FILE = os.environ.get('MODEL_FILE')

def removeUnwantedTokens(string_list):
    unwanted = ["UNKNOWN_TOKEN", "SENTENCE_START", "SENTENCE_END"]
    out = []
    for s in string_list:
        if not any([r in s for r in unwanted]):
            out.append(s)
    return out

def generate_sentence(model):
    # We start the sentence with the start token
    new_sentence = [word_to_index[sentence_start_token]]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[sentence_end_token]:
        next_word_probs = model.forward_propagation(new_sentence)
        sampled_word = word_to_index[unknown_token]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[unknown_token]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
    sentence_str = [index_to_word[x] for x in new_sentence[1:-1]]
    return sentence_str


def train_with_sgd(model, X_train, y_train, learning_rate=0.005, nepoch = 100, evaluate_loss_after = 5):
    # We keep track of the losses so we can plot them later
    losses = []
    num_examples_seen = 0
    for epoch in range(nepoch):
        # Optionally evaluate the loss
        if (epoch % evaluate_loss_after == 0):
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            print "%s: Loss after num_examples_seen=%d epoch=%d: %f" % (time, num_examples_seen, epoch, loss)
            # Adjust the learning rate if loss increases
            if (len(losses) > 1 and losses[-1][1] > losses[-2][1]):
                learning_rate = learning_rate * 0.5  
                print "Setting learning rate to %f" % learning_rate
            sys.stdout.flush()
            # ADDED! Saving model oarameters
            save_model_parameters_theano("./data/rnn-theano-%d-%d-%s.npz" % (model.hidden_dim, model.word_dim, time), model)
        # For each training example...
        for i in range(len(y_train)):
            # One SGD step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1

vocabulary_size = _VOCABULARY_SIZE
unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"


# Read the data and append SENTENCE_START and SENTENCE_END tokens
senTemp = []
print "Reading CSV file..."
with open('data/data.csv', 'rb') as f:
    reader = csv.reader(f, skipinitialspace=True)
    reader.next()
    # Split full comments into sentences
    sentences = itertools.chain(*[nltk.sent_tokenize(x[0].decode('utf-8').lower()) for x in reader])
    ArrSen = itertools.chain(*[nltk.sent_tokenize(x[0].decode('utf-8').lower()) for x in reader])
    # Append SENTENCE_START and SENTENCE_END
    sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
print "Parsed %d sentences." % (len(sentences))

# keep the number of sentences for later evualte Jaccard similarity 
num_sentences = len(sentences)
print "Number of sentences on orginal file %d " % num_sentences

# Tokenize the sentences into words
tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentences]

# Count the word frequencies
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
print "Found %d unique words tokens." % len(word_freq.items())

# Get the most common words and build index_to_word and word_to_index vectors
vocab = word_freq.most_common(vocabulary_size-1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])

print "Using vocabulary size %d." % vocabulary_size
print "The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1])

# Replace all words not in our vocabulary with the unknown token
for i, sent in enumerate(tokenized_sentences):
    tokenized_sentences[i] = [w if w in word_to_index else unknown_token for w in sent]

# Create the training data
X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])

# Creating a model object
model = RNNTheano(vocabulary_size, hidden_dim=_HIDDEN_DIM)

# Chekc if model loaded 
if _MODEL_FILE != None:
    load_model_parameters_theano(_MODEL_FILE, model)
# train the model with sgd 
losses = train_with_sgd(model, X_train, y_train, nepoch=_NEPOCH, learning_rate=_LEARNING_RATE, evaluate_loss_after=5)
# save the model
save_model_parameters_theano('./data/trained-model-theano.npz', model)
# load it to create random sentence
load_model_parameters_theano('./data/trained-model-theano.npz', model)

senten_min_length = 6
num_sentences = 50
newSen = [];

for i in range(num_sentences):
    sent = []
    # We want long sentences, not sentences with one or two words
    while len(sent) < senten_min_length:
        sent = generate_sentence(model)
    newSen.append(" ".join(sent))
# replace unwatned token before string matching
tokenized_old_sentences = []
for s in tokenized_sentences:
    tokenized_old_sentences.append( removeUnwantedTokens(s) )
    

tokenized_new_sentences = [nltk.word_tokenize(sent) for sent in newSen] 
print "first sentence is %s " % str(tokenized_new_sentences[1])
print "second sentence is %s " % str(tokenized_old_sentences[1])


avg = 0
minRate = 1
tmpValue = 0
tmpIndex = 0
index = 0 

for tmp_new in tokenized_new_sentences:
    for tmp_old in tokenized_old_sentences:
        newRate = distance.levenshtein( str(tmp_old),str(tmp_new) , 2)
        if minRate > newRate :
            minRate = newRate
            print "new min Rate : %f \t " % newRate
        if tmpValue != 0:
            tokenized_old_sentences[tmpIndex] = tmpValue
        tmpIndex = index
        tmpValue = minRate
        tokenized_old_sentences[index] = 0
        index += 1
    avg += minRate
    minRate = 0
    index = 0

avg = avg / num_sentences


print "levenshtein result is %f" % avg

# insert to new sentence to txt file
with open("Output2.txt", "w") as text_file:
    for arr in tokenized_new_sentences:
        for s in arr:
            text_file.write("%s " % s.encode("utf-8"))
        text_file.write("\n")
    text_file.write("Result: %f " % avg)
            
print "Finish!"
            
