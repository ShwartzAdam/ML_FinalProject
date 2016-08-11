#Deep Learning With RNN
Our project target was to use RNN deep learing algorithm to create a brand new text that will help us create a new anthem.

###Requirements:
```bash
appnope==0.1.0
backports.ssl-match-hostname==3.4.0.2
certifi==2015.9.6.2
decorator==4.0.2
funcsigs==0.4
functools32==3.2.3.post2
gnureadline==6.3.3
ipykernel==4.0.3
ipython==4.0.0
ipython-genutils==0.1.0
ipywidgets==4.0.2
Jinja2==2.8
jsonschema==2.5.1
jupyter==1.0.0
jupyter-client==4.0.0
jupyter-console==4.0.2
jupyter-core==4.0.6
MarkupSafe==0.23
matplotlib==1.4.3
mistune==0.7.1
mock==1.3.0
nbconvert==4.0.0
nbformat==4.0.0
nltk==3.0.5
nose==1.3.7
notebook==4.0.4
numpy==1.9.2
path.py==8.1.1
pbr==1.8.0
pexpect==3.3
pickleshare==0.5
ptyprocess==0.5
Pygments==2.0.2
pyparsing==2.0.3
python-dateutil==2.4.2
pytz==2015.4
pyzmq==14.7.0
qtconsole==4.0.1
scipy==0.16.0
simplegeneric==0.8.1
six==1.9.0
terminado==0.5
Theano==0.7.0
tornado==4.2.1
traitlets==4.0.0
wheel==0.26.0
```

##Process Description:

1) searched the web for united data of anthems in english (you can see the results under data/mydata.csv)


2) We used Theano to modulize the data set and prepared it to generate sentences.

the size of our vocabulary is pretty small considering our data set which contain only 219 national anthems so we kinda limited by how many uniqe words we could find.

hidden layer has set to 500 (as the “memory” of our network , making it bigger allows us to learn more complex patterns)
learing rate (which defines how big of a step we want to make in each iteration) was initialize to 0.005 and it goes on for 50 nepoch (number of times to iterate through the complete dataset).
```
_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '1000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '500')) 
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '50'))
```

3) after the model has finished training with train_with_sgd function, you can call it a 'smart model', and now you need to save it with save_model_parameters_theano function and the file will be 'trained-model-theano.npz' and saved at 'data' folder. (now we can use it)

4) we got the model , so now we use 'load_model_parameters_theano' function to load to model parameters and prepare it to generate sentences as much as we wish.
```
senten_min_length = x
num_sentences = y
```
5) after generating the sentences, we test the result by compare it facing the original sentences with 
Levenshtein distance (LD) which is a measure of the similarity between two strings.
every matching gave us a rate,and we calculated the avarage of all results.
```
# example how it works 
> distance.levenshtein(string_new,string_old)
> 0.761962 
```
6) Now we save the sentences in output.txt, and also the string matching summary result (from last step).


##Summery:

####Part of result:
#####We collected some of the sentences, those with some logic. 

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
