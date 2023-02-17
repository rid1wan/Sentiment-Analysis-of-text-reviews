# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.


## Dataset input
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import spacy
nlp = spacy.load('en_core_web_sm')

data_amazon = pd.read_csv('./drive/MyDrive/Datasets/Amazon.csv',encoding='utf8')

data_amazon.head()

review = data_amazon[['reviews.title','reviews.text','reviews.rating']]
review.head(25)

print(review.shape)

review['reviews.rating'].value_counts()

"""## Cleaning Dataset"""

review['clean_reviews'] = review['reviews.text'].str.replace('[^\w\s]','')
review['clean_reviews'] = review['clean_reviews'].astype(str)
review['clean_reviews'].head()

review.head(10)

import string

punct = string.punctuation

punct

from spacy.lang.en.stop_words import STOP_WORDS

stopwords = list(STOP_WORDS) # list of stopwords

def text_data_cleaning(clean_reviews):
  doc = nlp(clean_reviews)

  tokens = [] # list of tokens
  for token in doc:
    if token.lemma_ != "-PRON-":
      temp = token.lemma_.lower().strip()
    else:
      temp = token.lower_
    tokens.append(temp)
 
  cleaned_tokens = []
  for token in tokens:
    if token not in stopwords and token not in punct:
      cleaned_tokens.append(token)
  return cleaned_tokens

review['clean_token'] = review['clean_reviews'].apply(text_data_cleaning)
review.head(20)

"""## Sentiment Analyzer"""

!pip install nltk
import nltk

nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vadersentimentanalysis(clean_reviews):
    vs = analyzer.polarity_scores(clean_reviews)
    return vs['compound']

def calculate_sentiment(clean_token):

    scores = analyzer.polarity_scores(clean_token)
    
    Value_score = scores['compound']
   
    return Value_score

review['Value'] = review['clean_reviews'].apply(calculate_sentiment)

data_review= pd.DataFrame(review[['reviews.text', 'reviews.rating', 'Value']])
data_review.head(20)

def analysis(Value):
 if Value > 0:
    return 'Positive'
 else:
    return 'negative'

data_review ['Analysis'] = data_review['Value'].apply(analysis)
data_review.head(100)

from google.colab import drive
drive.mount('/content/drive')

"""## Getting ready for training"""

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.pipeline import Pipeline

tfidf = TfidfVectorizer(tokenizer=text_data_cleaning)

classifier = LinearSVC()

x = data_review['reviews.text'].fillna(' ')
y = data_review['Analysis'].fillna(' ')

"""## Train"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

x_train.shape, x_test.shape

x_train.head()

"""## Accuracy"""

clf = Pipeline([('tfidf',tfidf), ('clf',classifier)])

clf.fit(x_train, y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y_prediction = clf.predict(x_test)

confusion_matrix(y_test, y_prediction)

print(classification_report(y_test, y_prediction))

accuracy_score(y_test, y_prediction)

"""## Sentiment Prediction for new input"""

clf.predict(["It's too much hard to learn new things but I enjoy it"])

clf.predict(["Genorous but i will not buy it"])