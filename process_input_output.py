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

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger') # To get categorized wordslist

# list of woodward
woodward = pd.read_csv('woodward.csv', sep=",").columns.values.tolist()

# list of swadeshlist
swadesh = []
swa = pd.read_csv('swadeshList.csv', sep=",").columns.values.tolist()
for i in swa:
    swadesh.append(i.strip())

# print(swadesh)

# remove stop words (modeified: exclude wood or swadesh words from stop words list) from a list of words and returns unique words
def remove_stop_words_modified(w):
    stop_words = set(stopwords.words('english')) - set(woodward).union(set(swadesh))
    stop_words = stop_words.union('new','one','know','heads')
    return np.unique([wi for wi in w if not wi.lower() in stop_words])

# To get the words from each srt file (SPECIAL for AUSLAN)
def get_words_srt_aus(fileName):
    w = []

    try:
        file = open(fileName, 'r')
        lines = file.readlines()
        file.close()
    except IOError as e:
        print(e)

    for i in range(1, len(lines), 3):
        word_tokens = word_tokenize(lines[i].strip())
        filtered_word = remove_stop_words_modified(word_tokens)
        for each_filtered_word in filtered_word:
            if len(each_filtered_word.strip()) > 0:
                w.append(each_filtered_word.strip())
    
    return remove_stop_words_modified(w)

# To get the words from each vtt file (SPECIAL for AUSLAN)
def get_words_vtt_aus(fileName):
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

    return remove_stop_words_modified(w)

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


# To analyze swadesg and wood unsimilarity
def ana(videoFile, inWords, outWords):
    sw = [] # swadeshlisted word
    msw = []
    unmsw = []
    ww = [] # woodward word
    mww = []
    unmww = []

    outputWords = [x.lower() for x in outWords]
    outputWordsRoot = [stemmer.stem(x) for x in outputWords] # root
    outWordsSet = set(outputWords).union(set(outputWordsRoot))

    for word in inWords:
        if word.strip() in swadesh:
            sw.append(word)

        if word.strip() in swadesh:
            inWordsSet = set()
            synSet = {word, stemmer.stem(word)} # original + root
            syns = wordnet.synsets(word)
            for x in syns:
                syn = x.lemmas()[0].name()
                synSet.add(syn)
                synSet.add(stemmer.stem(syn)) # root
            inWordsSet = inWordsSet.union(synSet)

            if len(synSet.intersection(outWordsSet)) > 0:
                msw.append(word)

        if word.strip() in swadesh and word.strip() not in msw:
            unmsw.append(word)

        if word in woodward:
            ww.append(word)

        if word.strip() in woodward:
            inWordsSet = set()
            synSet = {word, stemmer.stem(word)} # original + root
            syns = wordnet.synsets(word)
            for x in syns:
                syn = x.lemmas()[0].name()
                synSet.add(syn)
                synSet.add(stemmer.stem(syn)) # root
            inWordsSet = inWordsSet.union(synSet)

            if len(synSet.intersection(outWordsSet)) > 0:
                mww.append(word)

        if word.strip() in woodward and word.strip() not in mww:
            unmww.append(word)


    global cat
    rec = [{"videoFile":videoFile, "groundTruthWords":inWords, "predictedWords":outWords, "SwadeshWords":sw, "matchedSwadeshWords":msw, "unmatchedSwadeshWords":unmsw, 
    "WoodWords":ww, "matchedWoodWords":mww, "unmatchedWoodWords":unmww}]
    print("====")
    print(rec)
    print("====")
    cat = pd.concat([cat, pd.DataFrame.from_records(rec)])

# To write in the dataframe
def writeToDataframe(videoFile, inWords, outWords):
    noun = [] # For Nouns
    adv = [] # For Adverbs
    adj = [] # For Adjectives
    vrb = [] # For Verbs
    poi = [] # For Prepositions like he, her, hers, etc.
    oth = [] # Others
    ww = [] # woodward word
    sw = [] # swadeshlisted word

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

        if word.strip() in swadesh:
            sw.append(word)

    global categories 
    record = [{"videoFile":videoFile, "groundTruthWords":inWords, "predictedWords":outWords,"Noun":noun, "Adverb":adv, "Adjective":adj, "Verb":vrb, "Pointers":poi, "others":oth, "woodward":ww, "swadesh":sw}]
    categories = pd.concat([categories, pd.DataFrame.from_records(record)])
# ------------------------------------------------------------------------------------------------------------------------------------------------

# PSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing PSL")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward", "swadesh"])

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
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])
inputDF = pd.read_csv('datasets/ISL/raw_ISL/ISL.csv')

for i in os.listdir('datasets/ISL/processed_ISL/vtt'): 
    if (i == '.DS_Store'):
        continue
    
    sen = inputDF['sentences'].iloc[int(i.removesuffix('_result.vtt'))]
    word_tokens = word_tokenize(sen.strip())
    inWords_isl = remove_stop_words(word_tokens)
    outWords_isl = get_words_vtt(f'datasets/ISL/processed_ISL/vtt/{i}')
    writeToDataframe(i.removesuffix('_result.vtt') + '.mp4', inWords_isl, outWords_isl)
    ana(i.removesuffix('.srt') + '.mp4', inWords_isl, outWords_isl)


cat.to_pickle('sw_ww_ISL')
cat.to_csv('sww_ww_ISL.csv', sep=",", index=False)

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


# AUSLAN---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUSLAN")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])

# For AUSLAN
for i in os.listdir('datasets/AUSLAN/processed_AUSLAN/srt'):
    if str(i) == ".DS_Store":
        continue
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_h2 = get_words_srt(f'datasets/AUSLAN/processed_AUSLAN/srt/{i}')
    outWords_h2 = get_words_vtt(f'datasets/AUSLAN/processed_AUSLAN/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)
    ana(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

cat.to_pickle('sw_ww_AUSLAN')
cat.to_csv('sww_ww_AUSLAN.csv', sep=",", index=False)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUSLAN.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# AUSLAN2---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUSLAN2")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])

# For AUSLAN2
for i in os.listdir('datasets/AUSLAN2/processed_AUSLAN/srt'):
    if str(i) == ".DS_Store":
        continue
    j = i.removesuffix('.srt') + '_result.vtt'
    # print(i, j)
    inWords_h2 = get_words_srt(f'datasets/AUSLAN2/processed_AUSLAN/srt/{i}')
    outWords_h2 = get_words_vtt(f'datasets/AUSLAN2/processed_AUSLAN/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)
    ana(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

cat.to_pickle('sw_ww_AUSLAN2')
cat.to_csv('sww_ww_AUSLAN2.csv', sep=",", index=False)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN2')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUSLAN2.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# AUSLAN3---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUSLAN3_where are you frog")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])

# For AUSLAN3
for i in os.listdir('datasets/AUSLAN3/processed_AUSLAN/srt'):
    if str(i) == ".DS_Store":
        continue
    j = i.removesuffix('.srt') + '_result.vtt'
    # print(i, j)
    inWords_h2 = get_words_srt(f'datasets/AUSLAN3/processed_AUSLAN/srt/{i}')
    outWords_h2 = get_words_vtt(f'datasets/AUSLAN3/processed_AUSLAN/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)
    ana(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

cat.to_pickle('sw_ww_AUSLAN3')
cat.to_csv('sww_ww_AUSLAN3.csv', sep=",", index=False)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN3')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUSLAN3.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# AUSLAN4  (AFL2c7a: where are you frog)---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUSLAN4_frog where are you")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])

# For AUSLAN4
for i in os.listdir('datasets/AUSLAN4/processed_AUSLAN/srt'):
    if str(i) == ".DS_Store":
        continue
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_h2 = get_words_srt_aus(f'datasets/AUSLAN4/processed_AUSLAN/srt/{i}')
    outWords_h2 = get_words_vtt_aus(f'datasets/AUSLAN4/processed_AUSLAN/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)
    ana(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

cat.to_pickle('sw_ww_AUSLAN4')
cat.to_csv('sww_ww_AUSLAN4.csv', sep=",", index=False)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN4')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUSLAN4.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# AUSLAN5  (PJHB2c7aLH: where are you frog)---------------------------------------------------------------------------------------------------------------------------------------------
# Processing the groundtruths and predictions to csv file
# define global variable for word category
print("Processing AUSLAN5_frog where are you")
categories = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "Noun", "Adverb", "Adjective", "Verb", "Pointers", "others", "woodward"])
cat = pd.DataFrame(columns = ["videoFile", "groundTruthWords", "predictedWords", "SwadeshWords", "matchedSwadeshWords", "unmatchedSwadeshWords", 
    "WoodWords", "matchedWoodWords", "unmatchedWoodWords"])

# For AUSLAN5 PJHB2c7aLH
for i in os.listdir('datasets/AUSLAN5/processed_AUSLAN/srt'):
    if str(i) == ".DS_Store":
        continue
    j = i.removesuffix('.srt') + '_result.vtt'
    inWords_h2 = get_words_srt(f'datasets/AUSLAN5/processed_AUSLAN/srt/{i}')
    outWords_h2 = get_words_vtt(f'datasets/AUSLAN5/processed_AUSLAN/vtt/{j}')
    writeToDataframe(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)
    ana(i.removesuffix('.srt') + '.mp4', inWords_h2, outWords_h2)

cat.to_pickle('sw_ww_AUSLAN5')
cat.to_csv('sww_ww_AUSLAN5.csv', sep=",", index=False)

categories.to_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN5')
categories.to_csv('processed_input_output/listOfSigns_inp-out_AUSLAN5.csv', sep=",", index=False)
# ------------------------------------------------------------------------------------------------------------------------------------------------

