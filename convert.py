import pandas as pd 
import numpy as np 

actualdf = pd.read_csv('Page Types/Sarie Toste (Right)/votes.csv')
outputdf = pd.read_csv('output_sarie_right.csv')

for i in range(len(outputdf)):
    outputdf['Actual'][i] = actualdf[actualdf['JPGNumber'] == outputdf['JPGNumber'][i]]['Race ' + str(outputdf['RaceNumber'][i])+ ' Bubble ' + str(outputdf['BubbleNumber'][i])].to_numpy()[0]
    
outputdf.to_csv('output_sarie_right.csv', index=False)