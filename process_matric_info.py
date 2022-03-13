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

# compare two lists of words with considering synnonym
def compare_Syn(inputWords, outputWords):
    count = 0

    outputWords = [x.lower() for x in outputWords]
    outWordsSet = set(outputWords)

    for s in inputWords:
        synSet = {s}
        syns = wordnet.synsets(s)
        for x in syns:
            synSet.add(x.lemmas()[0].name())
        if len(synSet.intersection(outWordsSet)) > 0:
            count += 1
        
    # print(len(inputWords))
    return count


def countMatched(inputDF):
    categories = pd.DataFrame(columns = ["videoFileName", 
    "totalWords", "totalNoun", "totalConj", "totalAdj", "totalVerbs", "totalAdv", "totalPoi", "totalMisce", 
    "matchedWords_noSyn", "matchedNoun_noSyn", "matchedConj_noSyn", "matchedAdj_noSyn", "matchedVerbs_noSyn", "matchedAdv_noSyn", "matchedPoi_noSyn", "matchedMisce_noSyn", "matchedSentence_noSyn", 
    "matchedWords_Syn", "matchedNoun_Syn", "matchedConj_Syn", "matchedAdj_Syn", "matchedVerbs_Syn", "matchedAdv_Syn", "matchedPoi_Syn", "matchedMisce_Syn", "matchedSentence_Syn"])

    for index, row in inputDF.iterrows():
        record = [{"videoFileName":row['videoFile'], 
        "totalWords":len(row['groundTruthWords']), "totalNoun":len(row['Noun']), "totalConj":None , "totalAdj":len(row['Adjective']), "totalVerbs":len(row['Verb']), "totalAdv":len(row['Adverb']), "totalPoi":len(row['Pointers']), "totalMisce":len(row['others']), 
        "matchedWords_noSyn":compare_noSyn(row['groundTruthWords'],row['predictedWords']), "matchedNoun_noSyn":compare_noSyn(row['Noun'],row['predictedWords']), "matchedConj_noSyn":None, "matchedAdj_noSyn":compare_noSyn(row['Adjective'],row['predictedWords']), "matchedVerbs_noSyn":compare_noSyn(row['Verb'],row['predictedWords']), "matchedAdv_noSyn":compare_noSyn(row['Adverb'],row['predictedWords']), "matchedPoi_noSyn":compare_noSyn(row['Pointers'],row['predictedWords']), "matchedMisce_noSyn":compare_noSyn(row['others'],row['predictedWords']), "matchedSentence_noSyn":0, 
        "matchedWords_Syn":compare_Syn(row['groundTruthWords'],row['predictedWords']), "matchedNoun_Syn":compare_Syn(row['Noun'],row['predictedWords']), "matchedConj_Syn":None, "matchedAdj_Syn":compare_Syn(row['Adjective'],row['predictedWords']), "matchedVerbs_Syn":compare_Syn(row['Verb'],row['predictedWords']), "matchedAdv_Syn":compare_Syn(row['Adverb'],row['predictedWords']), "matchedPoi_Syn":compare_Syn(row['Pointers'],row['predictedWords']), "matchedMisce_Syn":compare_Syn(row['others'],row['predictedWords']), "matchedSentence_Syn":0
        }]

        if record[0]['totalWords'] == 0 or record[0]['matchedWords_noSyn'] > 0:
            record[0]['matchedSentence_noSyn'] = 1

        if record[0]['totalWords'] == 0 or record[0]['matchedWords_Syn'] > 0:
            record[0]['matchedSentence_Syn'] = 1

        # global categories 
        categories = pd.concat([categories, pd.DataFrame.from_records(record)])

    return categories

# PSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_PSL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_PSL')

# ASL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-outto get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_ASL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_ASL')

# ISL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_ISL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_ISL')

# AUTSL---------------------------------------------------------------------------------------------------------------------------------------------
# Processing listOfSigns_inp-out to get how many matched

inputDF = pd.read_pickle('processed_input_output/listOfSigns_inp-out_AUTSL')
cat = countMatched(inputDF)
cat.to_pickle('processed_matrices/matrices_AUTSL')
