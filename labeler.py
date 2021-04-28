#USAGE: python3 labeler.py <dirname>
import sys
import os
import csv
import pandas as pd
import numpy as np
import easygui
import time

mark_dictionary = {'0': 'no mark',
                   '1': 'properly bubbled',
                   '2': 'X marked',
                   '3': 'check marked',
                   '4': 'bubbled and crossed out',
                   '5': 'poorly extracted',
                   '6': 'other mark',
                   'u': 'undo',
                   'p': 'print run info',
                   's': 'saves progress',
                   'q': 'saves and quits',
                   'qw/os': 'quits without saving'}

prompt = '---Menu---\n'
for i in mark_dictionary:
    prompt += i + ': ' + mark_dictionary[i] + '\n'

def makeDF(directory):
    with open(directory + '/labels.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        labels = ['path', 'result']
        csvwriter.writerow(labels)
        for filename in os.listdir(directory):
            if filename.endswith('_0.jpg'):
                csvwriter.writerow([filename ,'0'])
            elif filename.endswith('.jpg'):
                csvwriter.writerow([filename, '-1'])


def directoryIterator(directory):
    labelsdf = pd.read_csv(directory + '/labels.csv')
    numrows = labelsdf.count()['path']
    history = []
    row = 0
    while row < numrows:
        if labelsdf['result'].at[row] == -1:
            filePath = directory +'/' + labelsdf['path'].at[row]
            data = easygui.enterbox(msg=prompt, default=1, image=filePath)
            if data in mark_dictionary:
                if data == 'qw/os':
                    return
                elif data == 'u':
                    if len(history) != 0:
                        row = history.pop()
                        labelsdf['result'].at[row] = -1
                elif data == 'p':
                    string = 'Bubbles Labeled: ' +  str(len(history)) + '\n'
                    for i in history:
                        string += labelsdf['path'].at[i] + ': ' + str(labelsdf['result'].at[i]) + '\n'
                    easygui.msgbox(msg=string)
                elif data == 's':
                    labelsdf.to_csv(directory + '/labels.csv', index=False)
                    history = []
                elif data == 'q':
                    labelsdf.to_csv(directory + '/labels.csv', index=False)
                    return
                else:
                    labelsdf['result'].at[row] = data
                    history.append(row)
                    row += 1
        else:
            row += 1
    if easygui.ynbox(msg='Save?'):
        labelsdf.to_csv(directory + '/labels.csv', index=False)
directory = sys.argv[1]
if not os.path.exists(directory + '/labels.csv'):
    makeDF(directory)
directoryIterator(directory)

