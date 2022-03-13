from re import match
import nltk
import os
import pandas as pd

def combineCounts(datasetName):
    inputDF = pd.read_pickle(f'processed_matrices/matrices_{datasetName}')
    inputDF = inputDF.drop('videoFileName', axis=1)

    sumDF = inputDF.sum()
    sumDF = pd.concat([pd.Series({"totalVideos": inputDF.shape[0]}), sumDF])
    # sumDF["totalVideos"] = inputDF.shape[0]

    x = ["matchedWords", "matchedNoun", "matchedConj", "matchedAdj", "matchedVerbs", "matchedAdv", "matchedPoi", "matchedMisce", "matchedSentence"]
    y = ["totalWords", "totalNoun", "totalConj", "totalAdj", "totalVerbs", "totalAdv", "totalPoi", "totalMisce", "totalVideos"]

    for i in range(9):
        matchedNoSyn = x[i] + "_noSyn"
        matchedSyn = x[i] + "_Syn"
        percentNoSyn = x[i] + "_noSyn_percent"
        percentSyn = x[i] + "_Syn_percent"

        if(sumDF[y[i]] > 0):
            sumDF[percentNoSyn] = round(sumDF[matchedNoSyn] * 100 / sumDF[y[i]], 2)
            sumDF[percentSyn] = round(sumDF[matchedSyn] * 100 / sumDF[y[i]], 2)
        else: # devide by zero
            sumDF[percentNoSyn] = 100.0
            sumDF[percentSyn] = 100.0
    
    return sumDF.to_frame(name = datasetName)

sumDF = combineCounts('PSL')
sumDF = sumDF.join(combineCounts('ASL'))
sumDF = sumDF.join(combineCounts('ISL'))
sumDF = sumDF.join(combineCounts('AUTSL'))
print(sumDF)

sumDF.to_csv('matrices_final.csv', sep=',', index=True, index_label='Matrices')