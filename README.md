#Deep Learning With RNN
Our project target was to use RNN deep learing algorithm to create a brand new text that will help us create a new anthem.

###Requirements:
```bash
# Install requirements
Python, pip
pip install -r requirements.txt

# distance - Utilities for comparing sequences
https://github.com/doukremt/distance

# Start the notebook server , here you be running the code
jupyter notebook

```

##Process Description:

###1) Data search

#####searched the web for united data of anthems in english (you can see the results under data/mydata.csv)
(we planned on web scrapping but eventuly , we manage to allocate on raw csv file which already contained the anthems
writtin in english)

#####1.1) Preparations stage 
In that phase, we used simple known way to totaly remove all uneeded tokens.
```
reader = re.sub(r'[?|$|.|!|/|\|@|#|%|^|&|*|(|)]',r'',reader)
```
#####1.2) After the text has modifed to his clean state , we adding to each sentence tokens to sign them with open and end sentence mark so we could now which word open one and which word end, and finally split it to tokens.
```
# Append start token and end token
sentences = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in sentences]
# Tokenize the sentences into words
tokenized_sentences = [nltk.word_tokenize(sent) for sent in sentences]
```
##### 1.3) In that stage, we get the most common words to bulid our vocabulary 
which defined to 1000 because we didnt had much uniqe words so we made 0.25 the size of total uniqe words and this is becasue the size of our vocabulary is pretty small considering our data set which contain only 219 national anthems so we kinda limited by how many uniqe words we could find. index to words and oppsite phase.
```
# Get the most common words and build index_to_word and word_to_index vectors
word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
vocab = word_freq.most_common(vocabulary_size-1)
index_to_word = [x[0] for x in vocab]
index_to_word.append(unknown_token)
word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
# Replace all words not in our vocabulary with the unknown token
for i, sent in enumerate(tokenized_sentences):
    tokenized_sentences[i] = [w if w in word_to_index else unknown_token for w in sent]
```
###2) Modulize using Theano

hidden layer has set to 500 (as the “memory” of our network , making it bigger allows us to learn more complex patterns)
learing rate (which defines how big of a step we want to make in each iteration) was initialize to 0.005 and it goes on for 50 nepoch (number of times to iterate through the complete dataset).
```
_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '1000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '500')) 
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '50'))

model = RNNTheano(vocabulary_size, hidden_dim=_HIDDEN_DIM) 
# Train the model with sgd 
train_with_sgd(model, X_train, y_train, nepoch=_NEPOCH, learning_rate=_LEARNING_RATE, evaluate_loss_after=5)
```

###3) Save & load model and generate sentences

#### After the model has finished training with train_with_sgd function, you can call it a 'smart model', and now you need to save it with save_model_parameters_theano function and the model file type -> 'trained-model-theano.npz' will be save at 'data' folder. (now we can use it)
Here you can see that it will generate 50 sentences in the size of 6 .
```
# Save the model
save_model_parameters_theano('./data/trained-model-theano.npz', model)
# Load it to create random sentence
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

```

###4) Similarity between old and new sentences

##### After generating the sentences, we test the result by compare it facing the original sentences with 
Levenshtein distance (LD) which is a measure of the similarity between two strings.
every matching gave us a rate,and we calculated the avarage of all results.

####4.1) First of all we deleted the words that was sign with unkown token sign  , because they irrelevant for string matching
```
# old sentences
for s in tokenized_sentences:
    tokenized_old_sentences.append( removeUnwantedTokens(s) )
# new sentences
tokenized_new_sentences = [nltk.word_tokenize(sent) for sent in newSen]   

```

####4.2) We bulid a function that will find the best matching between old and new sentence , and return the heighst match.
```

for tmp_new in tokenized_new_sentences:
    for tmp_old in tokenized_old_sentences:
        newRate = distance.levenshtein( str(tmp_old),str(tmp_new) , 2)
        if minRate > newRate :
            minRate = newRate
        if tmpValue != 0:
            tokenized_old_sentences[tmpIndex] = tmpValue
        tmpIndex = index
        tmpValue = minRate
        tokenized_old_sentences[index] = 0
        index += 1
    avg += minRate
    minRate = 1
    index = 0

avg = avg / num_sentences

```
###5) Final step is to write it to Output file text
Save the sentences in output.txt, and also the string matching summary result (from last step).
```
# insert to new sentence to txt file
with open("Output2.txt", "w") as text_file:
    for arr in tokenized_new_sentences:
        for s in arr:
            text_file.write("%s " % s.encode("utf-8"))
        text_file.write("\n")
    text_file.write("Result: %f " % avg)
```

## Summary:

#### Part of result:
##### We collected some of the sentences, those with some logic. 

```
own been 's independence of sure people and forest nation . 
arise , angola , defenders children . 
freedom repeat truly or good salute ! 
oh on hail people over must tyrant . 
lived are free forefathers help our me . 
arise , my , fatherland and each reign past love reign . 
victory sure brave or you . 
```

For human eyes it's look not that good. But, if we trained the model for more iterations we could have a better results. 
The rates of our results was between 0.7 - 0.5 (from 1). 
