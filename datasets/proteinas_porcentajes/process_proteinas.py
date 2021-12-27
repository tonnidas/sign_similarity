from moviepy.editor import *

def split(f1, f2, out_prefix):

    file1 = open(f1, 'r')
    sentence = file1.readlines()
    file1.close()

    s = []

    for si in sentence:
        if ' --> ' in si:
            s.append(si.strip().split(' --> '))

    file2 = open(f2, 'r')
    word = file2.readlines()
    file2.close()

    w = []

    for i in range(len(word)):
        if ' --> ' in word[i]:
            x = word[i].strip().split(' --> ')
            x.append(word[i+1])
            w.append(x)

    out = []
    cur = []

    i = 0
    j = 0

    while i < len(s):
        cur = []
        while j < len(w):
            if (w[j][0] < s[i][1]):
                cur.append(w[j])
                j += 1
            else:
                break
        out.append(cur)
        i = i + 1

    for i in range(len(out)):
        
        ss = ""

        for j in range(len(out[i])):
            ss = ss + out[i][j][0] + ' --> ' + out[i][j][1] + '\n' + out[i][j][2] + '\n' 
        
        outFile = out_prefix + str(i+1) + '.srt'
        file3 = open(outFile, 'w')
        file3.write(ss)
        file3.close()

# convert videos to 25fps
for i in range (1, 171):
    clip = VideoFileClip(f'raw_proteinas_porcentajes/videos/{i}.mp4')
    clip.write_videofile(f'processed_proteinas_porcentajes/videos/proteinas_{i}.mp4', fps=25)

# split srt files
split('raw_proteinas_porcentajes/srt/proteinas_porcentajes.srt', 'raw_proteinas_porcentajes/srt/english_proteinas_porcentajes.srt', 'processed_proteinas_porcentajes/srt/proteinas_')
