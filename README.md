This repository checks for similarity between 
1) British sign language and Peruvian sign language 
2) British sign language and American sign language

with the sign-segmentation [model](https://github.com/tonnidas/sign-segmentation) that is pre-trained in British sign language (BSL).

![picture](how2sign.jpg)

We downloaded the files marked in the picture and then, we processed the video clips (trimmed according to srt file time per sentences) and English translations (stored each sentence of video in each srt files).

The processed Dataset (videos and srt files) is in **Processed_how2sign** folder. 

The processing code is in the files **.py**.