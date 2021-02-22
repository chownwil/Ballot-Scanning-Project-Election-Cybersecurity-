import pandas as pd 
import numpy as np 

actualdf = pd.read_csv('Page Types/Sarie Toste and Dan Hauser/votes.csv')
outputdf = pd.read_csv('output_sarie_dan.csv')

print(actualdf.shape)
print(outputdf.shape)

for i in range(len(outputdf)):
    outputdf['Actual'][i] = actualdf[actualdf['JPGNumber'] == outputdf['JPGNumber'][i]]['Race ' + str(outputdf['RaceNumber'][i])+ ' Bubble ' + str(outputdf['BubbleNumber'][i])].to_numpy()[0]
    
outputdf.to_csv('output_sarie_dan.csv', index=False)