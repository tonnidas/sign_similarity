import os
import pandas as pd
import numpy as np

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

# reading input and output folders to get comparative value ==============how2sign=====================
inputFiles = os.listdir('datasets/how2sign/processed_how2sign/srt')
outFiles = os.listdir('datasets/how2sign/processed_how2sign/vtt')

n = 50
matched = 0
empty = 0
c = 0
for f in inputFiles:
  str = f.split('.')
  for t in outFiles:
    if str[0] in t:
      c += 1

      inFile = f'datasets/how2sign/processed_how2sign/srt/{str[0]}.srt'
      outFile = f'datasets/how2sign/processed_how2sign/vtt/{str[0]}_result.vtt'

      inWords = get_words_srt(inFile)
      outWords = get_words_vtt(outFile)

      if len(inWords) == 0:
        print(f'Empty line: {i}')
        empty += 1
        continue 

      print(inWords)
      print("output: ",outWords)

      w, c = compare(inWords, outWords)
      if c > 0:
        matched += 1
        print(f'Line: {str[0]}.srt, words: {w}, matched: {c}, accuracy: {round(c*100/w, 2)}')
      break

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')