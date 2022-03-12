import pandas as pd
from moviepy.editor import *
import math
from nltk import word_tokenize
from nltk.corpus import stopwords
import string


# def processSentence(sentence):
#     stop = set(stopwords.words('english') + list(string.punctuation))
#     tokens = [i for i in word_tokenize(sentence.lower()) if i not in stop]
#     return " ".join(tokens)


# read csv file into df and sort by video length
df = pd.read_csv('/Users/tonni/Documents/sign_similarity/datasets/ISL/raw_ISL/ISL.csv', sep=',')
print(df['timestamp'])
# df['length'] = df['END_REALIGNED'] - df['START_REALIGNED']

cnt = 0
first = 0.00

for index, row in df.iterrows():
    # if row['length'] > 3 and row['length'] < 6:

        # print("hi: ", row['start'])
        cnt += 1

        # # split srt
        # time = f"{row['START_REALIGNED']} --> {row['END_REALIGNED']}"
        # sentence = time + '\n' + processSentence(row['SENTENCE'])
        # outfileName = f"processed_how2sign/srt/{row['SENTENCE_NAME']}.srt"
        # outfile = open(outfileName, 'w')
        # outfile.write(sentence)
        # outfile.close()

        # split video
        clip = VideoFileClip(f'/Users/tonni/Documents/sign_similarity/datasets/ISL/raw_ISL/ISL.mp4')
        a = row['timestamp'].split(':')
        f = (float(a[0])*60) + (float(a[1]))
        clip = clip.subclip(first, float(f))
        clip.write_videofile(f"/Users/tonni/Documents/sign_similarity/datasets/ISL/processed_ISL/{cnt}.mp4", fps=25)

        first = float(f)
        print(first)

        # if cnt == 3:
        #     break

print(cnt)