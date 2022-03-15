from re import match
import nltk
import os
import pandas as pd
import numpy as np
from os.path import exists # To check if a file exists

# To get the synonyms of words
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger') # To get categorized wordslist

# list of woodward
woodward = pd.read_csv('woodward.csv', sep=",").columns.values.tolist()

# remove stop words from a list of words and returns unique words
def remove_stop_words(w):
    stop_words = set(stopwords.words('english'))
    return np.unique([wi for wi in w if not wi.lower() in stop_words])

# To get the words from each srt file
def get_words_srt(fileName):
    w = []

    try:
        file = open(fileName, 'r')
        lines = file.readlines()
        file.close()
    except IOError as e:
        print(e)

    for i in range(1, len(lines), 3):
        word_tokens = word_tokenize(lines[i].strip())
        filtered_word = remove_stop_words(word_tokens)
        for each_filtered_word in filtered_word:
            if len(each_filtered_word.strip()) > 0:
                w.append(each_filtered_word.strip())
    
    return remove_stop_words(w)

# To get the words from each vtt file
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
        word = lines[i].strip().split(',')
        for j in range(0, len(word)):
            if ':' not in word[j] and '-' not in word[j] and '(' not in word[j]:
                w.append(word[j])

    return remove_stop_words(w)

# To write in the dataframe
def writeToDataframe(videoFile, inWords, outWords):
    noun = [] # For Nouns
    adv = [] # For Adverbs
    adj = [] # For Adjectives
    vrb = [] # For Verbs
    poi = [] # For Prepositions like he, her, hers, etc.
    oth = [] # Others
    ww = [] # woodward

    for word in inWords:
        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "NN") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "NNS") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "NNP") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "NNPS"):
            noun.append(word)

        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "RB") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "RBR") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "RBS"):
            adv.append(word)

        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "JJ") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "JJR") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "JJS"):
            adj.append(word)

        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VB") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VBG") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VBD") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VBN") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VBP") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "VBZ"):
            vrb.append(word)

        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "DT") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "PRP") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "PRP$"):
            poi.append(word)

        if (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "CC") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "PDT") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "CD") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "EX") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "IN") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "MD") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "POS") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "RP") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "TO") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "UH") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "FW") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "IN") or (nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "LS"):
            oth.append(word)

        if word in woodward:
            ww.append(word)

    global categories 
    record = [{"videoFile":videoFile, "groundTruthWords":inWords, "predictedWords":outWords,"Noun":noun, "Adverb":adv, "Adjective":adj, "Verb":vrb, "Pointers":poi, "others":oth, "woodward":ww}]
    categories = pd.concat([categories, pd.DataFrame.from_records(record)])
# ------------------------------------------------------------------------------------------------------------------------------------------------

# PSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing PSL")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])

# For ira
for i in os.listdir('datasets/ira_alegria/processed_ira_alegria/srt'):   
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_ira = get_words_srt(f'datasets/ira_alegria/processed_ira_alegria/srt/{i}')
    outWords_ira = get_words_vtt(f'datasets/ira_alegria/processed_ira_alegria/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_ira, outWords_ira)

# For proteinas
for i in os.listdir('datasets/proteinas_porcentajes/processed_proteinas_porcentajes/srt'):
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_pro = get_words_srt(f'datasets/proteinas_porcentajes/processed_proteinas_porcentajes/srt/{i}')
    outWords_pro = get_words_vtt(f'datasets/proteinas_porcentajes/processed_proteinas_porcentajes/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_pro, outWords_pro)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_PSL')
categories.to_csv('processed_input_output/listOfSigns_inp-out_PSL.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# ASL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing ASL")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])

# For how2sign
for i in os.listdir('datasets/how2sign/processed_how2sign/srt'):   
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_h1 = get_words_srt(f'datasets/how2sign/processed_how2sign/srt/{i}')
    outWords_h1 = get_words_vtt(f'datasets/how2sign/processed_how2sign/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h1, outWords_h1)

# For how2sign2
for i in os.listdir('datasets/how2sign2/processed_how2sign2/srt'):
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_h2 = get_words_srt(f'datasets/how2sign2/processed_how2sign2/srt/{i}')
    outWords_h2 = get_words_vtt(f'datasets/how2sign2/processed_how2sign2/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_ASL')
categories.to_csv('processed_input_output/listOfSigns_inp-out_ASL.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# ISL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing ISL")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
inputDF = pd.read_csv('datasets/ISL/raw_ISL/ISL.csv')

for i in os.listdir('datasets/ISL/processed_ISL/vtt'): 
    if (i == '.DS_Store'):
        continue
    
    sen = inputDF['sentences'].iloc[int(i.removesuffix('_result.vtt'))]
    word_tokens = word_tokenize(sen.strip())
    inWords_isl = remove_stop_words(word_tokens)
    outWords_isl = get_words_vtt(f'datasets/ISL/processed_ISL/vtt/{i}')
    writeToDataframe(i.removesuffix('_result.vtt') + '.mp4', inWords_isl, outWords_isl)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_ISL')
categories.to_csv('processed_input_output/listOfSigns_inp-out_ISL.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# AUTSL-------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUTSL")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
inputDF = pd.read_csv('datasets/AUTSL/raw_AUTSL/train_labels_merged.csv')

for i in os.listdir('datasets/AUTSL/processed_AUTSL/vtt'): 
    if (i == '.DS_Store'):
        continue
    
    # for AUTSL, we only have one word per video, convert it to a list of single word
    inWords_autsl = inputDF[inputDF['Name'] == i.removesuffix('_color_result.vtt')]['EN'].tolist()
    outWords_autsl = get_words_vtt(f'datasets/AUTSL/processed_AUTSL/vtt/{i}')
    writeToDataframe(i.removesuffix('_result.vtt') + '.mp4', inWords_autsl, outWords_autsl)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUTSL')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUTSL.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------