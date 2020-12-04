import pandas as pd 
import numpy as np

df = pd.read_csv('output.csv')

baseline_correct = 0
cnn_correct = 0

baseline_kick = 0
cnn_kick = 0

for i in range(len(df)):
    if df['Actual'][i] == df['Baseline'][i]:
        baseline_correct += 1
    elif df['Baseline'][i] == 2:
        baseline_correct += 1
        baseline_kick += 1
    if df['Actual'][i] == df['CNN'][i]:
        cnn_correct += 1
    elif df['CNN'][i] == 2:
        cnn_correct += 1
        cnn_kick += 1

print('Baseline Accuracy:', baseline_correct, ' / ', len(df))
print('Baseline Kick: ', baseline_kick)
print('CNN Accuracy:', cnn_correct, ' / ', len(df))
print('CNN Kick: ', cnn_kick)