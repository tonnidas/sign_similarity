import pandas as pd

dfClass = pd.read_csv('SignList_ClassId_TR_EN.csv')
dfTrain = pd.read_csv('train_labels_header.csv')

dfLabel = dfTrain.merge(dfClass, on="ClassId")
print(dfLabel)
dfLabel.to_csv('autsl_train_001.csv', sep=',', index=False)