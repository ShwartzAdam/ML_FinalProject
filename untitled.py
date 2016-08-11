
import csv
import nltk

tweets = read.csv("./data.csv", stringsAsFactors=FALSE)
library(tm)
library(SnowballC)
corpus = Corpus(VectorSource(tweets$Tweet))
corpus = tm_map(corpus, tolower)
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, removeWords, c("apple", stopwords("english")))
corpus = tm_map(corpus, stemDocument)
dtm = DocumentTermMatrix(corpus)
dtm


sparse = removeSparseTerms(dtm, 0.995)
sparse