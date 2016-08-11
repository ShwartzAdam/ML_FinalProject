
Requirements:
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

Summery:

1) First we search the web for united data of anthems in english (you can see the results under data/mydata.csv)

2) We modified menualy the data and remove unesesserly tokens

3) We used Theano to modulize the data set and prepared it to generate sentences.

the size of our vocabulary is pretty small considring our data set. we have in the data set only 219 national anthems so we kinda limited by how many uniqe words we could have.

hidden layer we set it to 500 (as the “memory” of our network , Making it bigger allows us to learn more complex patterns)
learing rate (which defines how big of a step we want to make in each iteration) was init to 0.005 and it goes on for 50 nepoch (number of times to iterate through the complete dataset).
```
_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '1000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '500')) 
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '50'))
```




