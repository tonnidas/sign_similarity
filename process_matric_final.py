from re import match
import nltk
import os
import pandas as pd

def combineCounts(inputDF):
    return

# PSL---------------------------------------------------------------------------------------------------------------------------------------------

inputDF = pd.read_pickle('processed_matrices/matrices_PSL')
cat = combineCounts(inputDF)
cat.to_pickle('processed_matrices/matrices_PSL')

# ASL---------------------------------------------------------------------------------------------------------------------------------------------

inputDF = pd.read_pickle('processed_matrices/matrices_ASL')
cat = combineCounts(inputDF)
cat.to_pickle('processed_matrices/matrices_ASL')

# ISL---------------------------------------------------------------------------------------------------------------------------------------------

inputDF = pd.read_pickle('processed_matrices/matrices_ISL')
cat = combineCounts(inputDF)
cat.to_pickle('processed_matrices/matrices_ISL')

# AUTSL---------------------------------------------------------------------------------------------------------------------------------------------

inputDF = pd.read_pickle('processed_matrices/matrices_AUTSL')
cat = combineCounts(inputDF)
cat.to_pickle('processed_matrices/matrices_AUTSL')
