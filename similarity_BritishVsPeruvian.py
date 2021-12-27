import os

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
      w.append(lines[i].strip())
  
  return w

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
# compare technique2 (synonym)

print('====================ira==========================')

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

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')

print('====================proteinas==========================')

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

print(f'Total lines: {n}, empty lines: {empty}, matched lines: {matched}, accuracy: {round(matched*100/(n-empty), 2)}')