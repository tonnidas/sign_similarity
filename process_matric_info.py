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

# compare two lists of words without considering synnonym
def compare_noSyn(inputWords, outputWords):
    count = 0
    for i in inputWords:
        for j in outputWords:
            if(i.lower() == j.lower()):
                count = count + 1
                break

    return count

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

# compare two lists of words with considering synnonym
def compare_Syn(inputWords, outputWords):
    count = 0

    outputWords = [x.lower() for x in outputWords]
    outputWordsRoot = [stemmer.stem(x) for x in outputWords] # root
    outWordsSet = set(outputWords).union(set(outputWordsRoot))


    inWordsSet = set()
    for s in inputWords:
    
        synSet = {s, stemmer.stem(s)} # original + root
        syns = wordnet.synsets(s)
        for x in syns:
            syn = x.lemmas()[0].name()
            synSet.add(syn)
            synSet.add(stemmer.stem(syn)) # root
        inWordsSet = inWordsSet.union(synSet)

        if len(synSet.intersection(outWordsSet)) > 0:
            count += 1
        
    return count


def compare_Syn_out(inputWords, outputWords):
    count = 0

    outputWords = [x.lower() for x in outputWords]
    out = set()
    for s in outputWords:
        out.add(s)
        syns = wordnet.synsets(s)
        for x in syns:
            out.add(x.lemmas()[0].name())

    # outWordsSet = set(outputWords)

    for s in inputWords:
        synSet = {s}
        syns = wordnet.synsets(s)
        for x in syns:
            synSet.add(x.lemmas()[0].name())
        if len(synSet.intersection(out)) > 0:
            count += 1
        
    return count


def countMatched(inputDF):
    categories = pd.DataFrame(columns = ["videoFileName", 
    "totalWords", "totalNoun", "totalConj", "totalAdj", "totalVerbs", "totalAdv", "totalPoi", "totalMisce", "totalWood", "totalSwadesh",
    "matchedWords_noSyn", "matchedNoun_noSyn", "matchedConj_noSyn", "matchedAdj_noSyn", "matchedVerbs_noSyn", "matchedAdv_noSyn", "matchedPoi_noSyn", "matchedMisce_noSyn", "matchedWood_noSyn", "matchedSwadesh_noSyn", "matchedSentence_noSyn", 
    "matchedWords_Syn", "matchedNoun_Syn", "matchedConj_Syn", "matchedAdj_Syn", "matchedVerbs_Syn", "matchedAdv_Syn", "matchedPoi_Syn", "matchedMisce_Syn", "matchedWood_Syn", "matchedSwadesh_Syn", "matchedSentence_Syn",
    "matchedWords_Syn_out", "matchedNoun_Syn_out", "matchedConj_Syn_out", "matchedAdj_Syn_out", "matchedVerbs_Syn_out", "matchedAdv_Syn_out", "matchedPoi_Syn_out", "matchedMisce_Syn_out", "matchedWood_Syn_out", "matchedSwadesh_Syn_out", "matchedSentence_Syn_out"])



    for index, row in inputDF.iterrows():
        record = [{"videoFileName":row['videoFile'], 
        "totalWords":len(row['groundTruthWords']), "totalNoun":len(row['Noun']), "totalConj":0 , "totalAdj":len(row['Adjective']), "totalVerbs":len(row['Verb']), "totalAdv":len(row['Adverb']), "totalPoi":len(row['Pointers']), "totalMisce":len(row['others']), "totalWood":len(row['woodward']), "totalSwadesh":len(row['swadesh']), 
        "matchedWords_noSyn":compare_noSyn(row['groundTruthWords'],row['predictedWords']), "matchedNoun_noSyn":compare_noSyn(row['Noun'],row['predictedWords']), "matchedConj_noSyn":0, "matchedAdj_noSyn":compare_noSyn(row['Adjective'],row['predictedWords']), "matchedVerbs_noSyn":compare_noSyn(row['Verb'],row['predictedWords']), "matchedAdv_noSyn":compare_noSyn(row['Adverb'],row['predictedWords']), "matchedPoi_noSyn":compare_noSyn(row['Pointers'],row['predictedWords']),"matchedMisce_noSyn":compare_noSyn(row['others'],row['predictedWords']), "matchedWood_noSyn":compare_noSyn(row['woodward'],row['predictedWords']), "matchedSwadesh_noSyn":compare_noSyn(row['swadesh'],row['predictedWords']), "matchedSentence_noSyn":0, 
        "matchedWords_Syn":compare_Syn(row['groundTruthWords'],row['predictedWords']), "matchedNoun_Syn":compare_Syn(row['Noun'],row['predictedWords']), "matchedConj_Syn":0, "matchedAdj_Syn":compare_Syn(row['Adjective'],row['predictedWords']), "matchedVerbs_Syn":compare_Syn(row['Verb'],row['predictedWords']), "matchedAdv_Syn":compare_Syn(row['Adverb'],row['predictedWords']), "matchedPoi_Syn":compare_Syn(row['Pointers'],row['predictedWords']), "matchedMisce_Syn":compare_Syn(row['others'],row['predictedWords']), "matchedWood_Syn":compare_Syn(row['woodward'],row['predictedWords']), "matchedSwadesh_Syn":compare_Syn(row['swadesh'],row['predictedWords']), "matchedSentence_Syn":0,
        "matchedWords_Syn_out":compare_Syn_out(row['groundTruthWords'],row['predictedWords']), "matchedNoun_Syn_out":compare_Syn_out(row['Noun'],row['predictedWords']), "matchedConj_Syn":0, "matchedAdj_Syn_out":compare_Syn_out(row['Adjective'],row['predictedWords']), "matchedVerbs_Syn_out":compare_Syn_out(row['Verb'],row['predictedWords']), "matchedAdv_Syn_out":compare_Syn_out(row['Adverb'],row['predictedWords']), "matchedPoi_Syn_out":compare_Syn_out(row['Pointers'],row['predictedWords']), "matchedMisce_Syn_out":compare_Syn_out(row['others'],row['predictedWords']), "matchedWood_Syn_out":compare_Syn_out(row['woodward'],row['predictedWords']), "matchedSwadesh_Syn_out":compare_Syn_out(row['swadesh'],row['predictedWords']), "matchedSentence_Syn_out":0
        }]

        if record[0]['totalWords'] == 0 or record[0]['matchedWords_noSyn'] > 0:
            record[0]['matchedSentence_noSyn'] = 1

        if record[0]['totalWords'] == 0 or record[0]['matchedWords_Syn'] > 0:
            record[0]['matchedSentence_Syn'] = 1

        if record[0]['totalWords'] == 0 or record[0]['matchedWords_Syn_out'] > 0:
            record[0]['matchedSentence_Syn_out'] = 1

        categories = pd.concat([categories, pd.DataFrame.from_records(record)])

    return categories

# PSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_PSL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_PSL')
cat.to_csv('processed_matrices/matrices_PSL.csv', sep=",")

# ASL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-outto get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_ASL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_ASL')
cat.to_csv('processed_matrices/matrices_ASL.csv', sep=",")

# ISL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_ISL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_ISL')
cat.to_csv('processed_matrices/matrices_ISL.csv', sep=",")

# AUTSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUTSL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUTSL')
cat.to_csv('processed_matrices/matrices_AUTSL.csv', sep=",")

# AUSLAN---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUSLAN')
cat.to_csv('processed_matrices/matrices_AUSLAN.csv', sep=",")

# AUSLAN2---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN2')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUSLAN2')
cat.to_csv('processed_matrices/matrices_AUSLAN2.csv', sep=",")

# AUSLAN3---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN3')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUSLAN3')
cat.to_csv('processed_matrices/matrices_AUSLAN3.csv', sep=",")

# AUSLAN4---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN4')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUSLAN4')
cat.to_csv('processed_matrices/matrices_AUSLAN4.csv', sep=",")

# AUSLAN5---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUSLAN5')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUSLAN5')
cat.to_csv('processed_matrices/matrices_AUSLAN5.csv', sep=",")