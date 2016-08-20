#Deep Learning With RNN
Our project target was to use RNN deep learing algorithm to create a brand new text that will help us create a new anthem.

###Requirements:
```bash
# Install requirements
pip install -r requirements.txt

# Start the notebook server , here you be running the code
jupyter notebook

# distance - Utilities for comparing sequences
https://github.com/doukremt/distance

# igraph libary
pip install python-igraph
```

##Process Description:

###1) searched the web for united data of anthems in english (you can see the results under data/mydata.csv)
(we planned on web scrapping but eventuly , we manage to allocate on raw csv file which already contained the anthems
writtin in english)

####1.1) Preparations stage 
In that phase, we used simple known way to totaly remove all uneeded tokens , including countries name.
  
###2) We used Theano to modulize the data set and prepared it to generate sentences.
the size of our vocabulary is pretty small considering our data set which contain only 219 national anthems so we kinda limited by how many uniqe words we could find.

hidden layer has set to 500 (as the “memory” of our network , making it bigger allows us to learn more complex patterns)
learing rate (which defines how big of a step we want to make in each iteration) was initialize to 0.005 and it goes on for 50 nepoch (number of times to iterate through the complete dataset).
```
_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '1000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '500')) 
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '50'))
```

###3) after the model has finished training with train_with_sgd function, you can call it a 'smart model', and now you need to save it with save_model_parameters_theano function and the file will be 'trained-model-theano.npz' and saved at 'data' folder. (now we can use it)

###4) we got the model , so now we use 'load_model_parameters_theano' function to load to model parameters and prepare it to generate sentences as much as we wish.
```
senten_min_length = x
num_sentences = y
```
###5) after generating the sentences, we test the result by compare it facing the original sentences with 
Levenshtein distance (LD) which is a measure of the similarity between two strings.
every matching gave us a rate,and we calculated the avarage of all results.
```
# example how it works 
> distance.levenshtein(string_new,string_old)
> 0.761962 
```
###6) Now we save the sentences in output.txt, and also the string matching summary result (from last step).


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
