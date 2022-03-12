import os
from moviepy.editor import *
filepath = f'/Users/tonni/Documents/AUTSL/train_001'

# convert videos to 25fps
for video in os.listdir(filepath):
    if 'color' in video:
        clip = VideoFileClip(f'/Users/tonni/Documents/AUTSL/train_001/{video}')
        print(video)
        clip.write_videofile(f'/Users/tonni/Documents/AUTSL/train_001_25fps/{video}', fps=25)