from re import match
import nltk
import os
import pandas as pd
import numpy as np
from os.path import exists # To check if a file exists

# To get the synonyms of words
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger') # To get categorized wordslist

# list of swadeshlist
swadesh = pd.read_csv('swadeshList.csv', sep=",").columns.values.tolist()

stop_words = set(stopwords.words('english'))
print(stop_words)

print()
print()

s = []
for i in swadesh:
    for j in stop_words:
        if i.lower()==j.lower():
            s.append(j)

print(s)