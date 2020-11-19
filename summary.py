from PIL import Image
import sys
import csv
import pandas as pd
import numpy as np

"""
Run: In Terminal or CommandPrompt, call using "python labelling.py start_ballot_num end_ballot_num"

Usage: Then the start_ballot will be opened, and you will be prompted (in Terminal or CommandPrompt) to
enter a string. The format of the string should be 'first_vote', 'second_vote', 'third_vote'. Candidate numbers
start at 1, and should be in order as they appear on the ballot. If fewer than 3 candidates are voted for, the
last votes should be '0'. After entering a correct vote, the next image will pop up. Then just repeat until the
end_ballot.

Valid usage: '135', '120', '300', '000'

Invalid usage: '1 3 5', '1,3,5', '102', '314'

"""
page_layout_bubbles = {'Zachary B. Thoma and Dan Hauser': [7, 3],
                       'David R. Couch': [9],
                       'Kathleen A. Fairchild': [7],
                       'Nicole Chase': [7],
                       'Michael Caldwell': [5],
                       'Natalie Zall': [8],
                       'Sarie Toste Zachary B. Thoma and Dan Hauser': [7, 7, 3],
                       'Sherry Dalziel': [7],
                       'Kerry Gail Watty': [3],
                       'Sarie Toste (left)': [7],
                       'Emil Feierabend and Jerry Hansen': [3, 8],
                       'Sarie Toste and Dan Hauser': [7, 3],
                       'Sarie Toste (right)': [7],
                       'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       'Tim Hooven': [8],
                       'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       'Gaye Gerdts': [3]
                       }

mark_dictionary = {
    '-1': 'unlabeled',
    '0': 'no mark',
    '1': 'properly bubbled',
    '2': 'X marked',
    '3': 'check marked',
    '4': 'lightly bubbled',
    '5': 'partially bubbled',
    '6': 'bubbled and crossed out',
    '7': 'bad scan / wrong race',
    '8': 'other'}

total_mark_counts = np.zeros(len(mark_dictionary))

pagesdf = pd.read_csv('pages.csv')

with open('summary.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    header = ['Page Type']
    header.append('Bubbling Status')
    header.append('labeled')
    for i in mark_dictionary:
        header.append(mark_dictionary[i])
    csvwriter.writerow(header)

    for pl in page_layout_bubbles:
        pldf = pd.read_csv('Page Types/' + pl + '/labels.csv')
        mark_counts = np.zeros(len(mark_dictionary))
        for ballot in range(0, len(pldf.index)):
            for race in range(0, len(page_layout_bubbles[pl])):
                for bubble in range(0, page_layout_bubbles[pl][race]):
                    mark_counts[pldf['Race ' +
                                     str(race) + ' Bubble ' + str(bubble)][ballot] + 1] += 1

        for mark in range(0, len(mark_counts)):
            total_mark_counts[mark] += mark_counts[mark]

        output_string = [pl]
        if mark_counts[0] == 0:
            output_string.append('Complete')
        else:
            output_string.append('Incomplete')
        labeled = 0
        for mark in mark_counts:
            labeled += mark
        output_string.append(str(int(labeled)))
        for mark in range(0, len(mark_counts)):
            output_string.append(str(int(mark_counts[mark])))
        csvwriter.writerow(output_string)

    output_string = ['Total']
    if total_mark_counts[0] == 0:
        output_string.append('Complete')
    else:
        output_string.append('Incomplete')
    labeled = 0
    for mark in total_mark_counts:
        labeled += mark
    output_string.append(str(int(labeled)))
    for mark in range(0, len(total_mark_counts)):
        output_string.append(str(int(total_mark_counts[mark])))
    csvwriter.writerow(output_string)
