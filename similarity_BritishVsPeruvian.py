import os
import pandas as pd
import numpy as np

# To get the synonyms of words
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

def get_words_srt(fileName):
  w = []
  lines = []

  try:
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
  except IOError as e:
    print(e)

  for i in range(1, len(lines), 3):
    s = lines[i].strip()
    if(len(s) > 0):
      w.append(s)
  
  return w

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


# compare technique1 (nlt - lemmatizing - root of the word)

# # compare two lists of words  
# def compare(inputWords, outputWords):
#   count = 0

#   for i in inputWords:
#     for j in outputWords:
#       if(i.lower() == j.lower()):
#         count = count + 1
#         break

#   return len(inputWords), count

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
      
  return len(inputWords), count

print('====================ira==========================')

# define global variable for word category
categories = pd.DataFrame(columns = ["word", "category", "matched"])

total_words = 0
got_words = 0

n = 53
matched = 0
empty = 0

for i in range(1, n+1):
  inFile = f'datasets/ira_alegria/processed_ira_alegria/srt/ira_{i}.srt'
  outFile = f'datasets/ira_alegria/processed_ira_alegria/vtt/ira_{i}_result.vtt'

  inWords = get_words_srt(inFile)
  outWords = get_words_vtt(outFile)

  if len(inWords) == 0:
    print(f'Empty line: {i}')
    empty += 1
    continue 
  
  w, c = compare(inWords, outWords)
  if c > 0:
    matched += 1
    print(f'Line: {i}, words: {w}, matched: {c}, accuracy: {round(c*100/w, 2)}')

  w1, c1 = compareSynonyms(inWords, outWords)
  total_words = total_words + w1
  got_words = got_words + c1

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')
per = (got_words/total_words)*100
print("Total words = ",total_words," matched words = ", got_words," accuracy percentage = ",per)

categories.to_csv('datasets/ira_alegria/output_ira/category.csv', sep='\t')

df = categories.groupby('category')['matched'].agg(['sum', 'count'])
df['percent'] = df['sum'] * 100 / df['count']
print(df)

print('====================proteinas==========================')

# define global variable for word category
categories = pd.DataFrame(columns = ["word", "category", "matched"])

total_words = 0
got_words = 0

n = 144
matched = 0
empty = 0

for i in range(1, n+1):
  inFile = f'datasets/proteinas_porcentajes/processed_proteinas_porcentajes/srt/proteinas_{i}.srt'
  outFile = f'datasets/proteinas_porcentajes/processed_proteinas_porcentajes/vtt/proteinas_{i}_result.vtt'

  inWords = get_words_srt(inFile)
  outWords = get_words_vtt(outFile)
  
  if len(inWords) == 0:
    print(f'Empty line: {i}')
    empty += 1
    continue 

  w, c = compare(inWords, outWords)
  if c > 0:
    matched += 1
    print(f'Line: {i}, words: {w}, matched: {c}, accuracy: {round(c*100/w, 2)}')

  w1, c1 = compareSynonyms(inWords, outWords)
  total_words = total_words + w1
  got_words = got_words + c1

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')
per = (got_words/total_words)*100
print("Total words = ",total_words," matched words = ", got_words," accuracy percentage = ",per)

categories.to_csv('datasets/proteinas_porcentajes/output_proteinas/category.csv', sep='\t')

df = categories.groupby('category')['matched'].agg(['sum', 'count'])
df['percent'] = df['sum'] * 100 / df['count']
print(df)