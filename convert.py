import pandas as pd 
import numpy as np 

actualdf = pd.read_csv('sherry_dalziel_actual.csv')
actualarr = actualdf.to_numpy()
outputdf = pd.read_csv('output.csv')

print(actualarr.shape)
print(outputdf.shape)

for i in range(len(actualdf)):
    for j in range(1, 8):
        outputdf['Actual'][7 * i + j - 1] = actualarr[i][j]

outputdf.to_csv('output3.csv', index=False)