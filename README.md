# Similarity checking of sign languages

This repository checks for similarity between 
1) BSL & ASL 
2) BSL & Auslan
3) BSL & ISL

with a segmentation [model](https://github.com/tonnidas/sign-segmentation) from "Temporal segmentation of sign language videos" that is pre-trained in British sign language (BSL).

Although we have represented these three compararishn (as we found existing comaparative values for these three only) in 0ur paper "A Machine Learning-based Segmentation Approach for Measuring Similarity Between Sign Languages", we worked with total of 5 datasets for experimentation and kept them in our repository.


## Contents
<!-- ![picture](contents.png) -->
The `datasets` folder has total of $5$ datasets, namely Auslan, ASL, AUTSL and ISL. for preprocessing purposes, there are multiple folders for each datasets. 
- For Auslan dataset, we have a total of $5$ folders namely AUSLAN, AUSLAN2, AUSLAN3, AUSLAN4, AUSLAN5. 
- For ASL dataset, we have a total of 2 folders namely, how2sign and how2sign2. 
- For ISL we have only one folder named as ISL.
- For Autsl we have only one folder named AUTSL. 
All these folders have a common structure. They have core 3 subfolders named as output, processed, raw along with some .py files made to preprocess the dataset. 
-  `Here:-`
    1. `processed_dataset name`: Inside the processed subfolder, there are three more subsubfolders namely, srt, video, vtt. , input videos, output segmented signs accordingly. Srt folder contains the ground truth files in srt for each sentence. vtt folder contains the predicted files of each of those sentences. Video folder holds the video files for each of those sentences. 
    2. `raw_dataset name`: It has `srt`, `videos` folders holding the signs with temporal boundaries, input videos accordingly.
    3. `process_dataset name.py:` This is the model we implemented to process the raw  dataset. Processed folder is the one where we put our final pre-processed dataset. 
- Other than dataset folder, we have two more important folders namely, `processed_input_output`, `processed_matrices`. There are also .py files named as *processed_input_output.py*, *processed_matrices.py* and a final output generator .py file namely *processed_output*. As our project grew, we partitioned different steps of our code work to keep track of step by step results. 
- We have used some pickles in similar fashioned names to store result and information along with storing them in csv for later use purpose. 


## Setups
All set up instructions for "Temporal segmentation of sign language videos" can be found [here](https://github.com/tonnidas/sign-segmentation). The other pre-processing models are python files. 


### Models
The models for pre-processing the datasets are attached in the `datasets folder`. And the segmentation model that we modified for our experiment is in [here](https://github.com/tonnidas/sign-segmentation).

## Results
- A summary of or results are shown in *summary.xlsx* and an elaborated version of the main result is shown in *matrices_final*

<!-- ![ira_alegria result](ira.png) ![proteinas result](prro.png) -->



<!-- ![how2sign result](how2sign.png) -->