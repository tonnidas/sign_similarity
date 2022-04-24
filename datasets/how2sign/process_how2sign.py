import pandas as pd
from moviepy.editor import *
import math
from nltk import word_tokenize
from nltk.corpus import stopwords
import string


def processSentence(sentence):
    stop = set(stopwords.words('english') + list(string.punctuation))
    tokens = [i for i in word_tokenize(sentence.lower()) if i not in stop]
    return " ".join(tokens)


# read csv file into df and sort by video length 
df = pd.read_csv('raw_how2sign/srt/how2sign_realigned_test.csv', sep='\t')
df['length'] = df['END_REALIGNED'] - df['START_REALIGNED']

cnt = 0

for index, row in df.iterrows():
    if row['length'] > 3 and row['length'] < 6:
        cnt += 1

        # split srt

        time = f"{row['START_REALIGNED']} --> {row['END_REALIGNED']}"
        sentence = time + '\n' + processSentence(row['SENTENCE'])
        outfileName = f"processed_how2sign/srt/{row['SENTENCE_NAME']}.srt"
        outfile = open(outfileName, 'w')
        outfile.write(sentence)
        outfile.close()

        # split video

        clip = VideoFileClip(f"raw_how2sign/videos/{row['VIDEO_NAME']}.mp4")
        clip = clip.subclip(math.floor(
            row['START_REALIGNED']), math.ceil(row['END_REALIGNED']))
        clip.write_videofile(
            f"processed_how2sign/videos/{row['SENTENCE_NAME']}.mp4", fps=25)

        if cnt == 50:
            break

print(cnt)
