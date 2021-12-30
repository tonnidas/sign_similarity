from re import match
import nltk

import os
import pandas as pd
import numpy as np

# To get the synonyms of words
from nltk.corpus import wordnet
# nltk.download('wordnet')

# To check if a file exists
from os.path import exists

# To get categorized wordslist
nltk.download('averaged_perceptron_tagger')

# To get words' list from .srt file
def get_words_srt(fileName):
  w = []
  lines = []

  try:
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
  except IOError as e:
    print(e)

  words = lines[1].split(' ')
  myWordsList = np.unique(words)
  
  return myWordsList   

# To get words' list from .vtt file
def get_words_vtt(fileName):
  w = []
  lines = []

  try:
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
  except IOError as e:
      print(e)

  for i in range(3, len(lines), 3):
    ww = ''

    for c in lines[i]:
      if c.isalpha():
        ww = ww + c
      elif len(ww) > 0:
        w.append(ww)
        ww = ''
    
    if len(ww) > 0:
      w.append(ww)

  return w

# compare two lists of words  
def compare(inputWords, outputWords):
  count = 0

  for i in inputWords:
    for j in outputWords:
      if(i.lower() == j.lower()):
        count = count + 1
        break

  return len(inputWords), count

# compare technique2 (synonym)
def compareSynonyms(inputWords, outputWords):
  count = 0

  outputWords = [x.lower() for x in outputWords]
  outWordsSet = set(outputWords)

  for s in inputWords:
    synSet = {s}

    syns = wordnet.synsets(s)
    for x in syns:
      synSet.add(x.lemmas()[0].name())

    matched = 0

    if(len(synSet.intersection(outWordsSet)) > 0):
      count += 1
      matched = 1

    # find word category
    tag = nltk.pos_tag(nltk.word_tokenize(s))[0][1]
    global categories 
    categories = categories.append({"word": s, "category": tag, "matched": matched}, ignore_index = True)
    
    # print(synSet)
    # print(outWordsSet)
    # print(count)
    # print("====")
      
  return len(inputWords), count
    

# reading input and output folders from how2sign to get comparative value ==============how2sign=====================
inputFiles = os.listdir('datasets/how2sign/processed_how2sign/srt')
outFiles = os.listdir('datasets/how2sign/processed_how2sign/vtt')

# define global variable for word category
categories = pd.DataFrame(columns = ["word", "category", "matched"])

total_words = 0
got_words = 0

n = 50
matched = 0
empty = 0
count = 0

for f in inputFiles:
  str = f.split('.')
  for t in outFiles:
    if str[0] in t:
      count += 1

      inFile = f'datasets/how2sign/processed_how2sign/srt/{str[0]}.srt'
      outFile = f'datasets/how2sign/processed_how2sign/vtt/{str[0]}_result.vtt'

      inWords = get_words_srt(inFile)
      outWords = get_words_vtt(outFile)

      if len(inWords) == 0:
        print(f'Empty line: {f}')
        empty += 1
        continue

      w, c = compare(inWords, outWords)
      print(w, c)
      print("===========================")
      if c > 0:
        matched += 1
        print(f'Line: {str[0]}.srt, words: {w}, matched: {c}, accuracy: {round(c*100/w, 2)}'+" ============= count: "+f'{count}')
      else:
        print("c: ", c)

      w1, c1 = compareSynonyms(inWords, outWords)
      total_words = total_words + w1
      got_words = got_words + c1
      print("w1: ",w1,"c1: ",c1)
      break

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')
print(total_words, got_words)

categories.to_csv('datasets/how2sign/output_how2sign/category.csv', sep='\t')

df = categories.groupby('category')['matched'].agg(['sum', 'count'])
df['percent'] = df['sum'] * 100 / df['count']
print(df)
# print(categories.groupby('category')['matched'].mean().reset_index())