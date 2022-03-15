from re import match
import nltk
import os
import pandas as pd

a = []

b = pd.read_pickle('processed_input_output/listOfSigns_inp-out_PSL')
print(b['groundTruthWords'][0])
c = pd.read_csv('woodward.csv')
print(c)
for i in range(len(b)):
    a.append([b['groundTruthWords'][i] for i in range(len(b['groundTruthWords'])) if b['groundTruthWords'][i] == "yes"])


print(a)