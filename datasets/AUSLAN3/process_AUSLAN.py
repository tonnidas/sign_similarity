import pandas as pd
import numpy as np
from moviepy.editor import *

# To get the synonyms of words
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ----------------------------------------------------------------------------------------------
# read csv file into df and sort by video length
file = open('raw_AUSLAN/srt/MAHB2c7aLH.srt')
lines = file.readlines()


# list of woodward
woodward = pd.read_csv('../../woodward.csv', sep=",").columns.values.tolist()
set1 = set(woodward)

# list of swadeshlist
swadesh = []
swa = pd.read_csv('../../swadeshList.csv', sep=",").columns.values.tolist()
for i in swa:
    swadesh.append(i.strip())
set2 = set(swadesh)

# stop_words = set(stopwords.words('english')) - set(['do', 'few', 'has', 'won', 'him', 'what', 'their', 'some', 'themselves', 'you', 'only', 'those', 'they', 'over' 'she', 'why', 'when', 'your', 'ourselves', 'who', 'that', 'not', 'he', 'own', 'there', 'yours', 'and', 'doing', 'them', 'yourself', 'how', 'where', 'which', 'no', 'yourselves', 'the', 'we', 'his', 'her'])
stop_words = set(stopwords.words('english')) - set1.union(set2)
print("Original stopwords length = ",len(set(stopwords.words('english'))),"modified stopwords length = ",len(stop_words))

c = 1
for i in range(1, len(lines), 4):
    # print(lines[i])

    # creating individual srt files
    file_out = open('processed_AUSLAN/srt/' + 'aus_' + str(c) + '.srt', 'w')
    file_out.write(lines[i])
    file_out.write(lines[i+1])
    file_out.close()


    # split video
    x = lines[i].strip().split(' --> ')
    start = x[0].replace(",", ".")
    end = x[1].replace(",", ".")
    clip = VideoFileClip(f"VideosGlosados156/MAHB2c7a.mp4")
    clip = clip.subclip(start, end)
    clip.write_videofile(f"processed_AUSLAN/videos/aus_{c}.mp4", fps=25)

    c += 1

# clip = VideoFileClip(f'ADCB2c7a.mp4')