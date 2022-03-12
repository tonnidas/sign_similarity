from re import match
import nltk
import os
import pandas as pd
import numpy as np

# To get the synonyms of words
from nltk.corpus import wordnet

# nltk.download('wordnet')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# To check if a file exists
from os.path import exists

# To get categorized wordslist
nltk.download('averaged_perceptron_tagger')