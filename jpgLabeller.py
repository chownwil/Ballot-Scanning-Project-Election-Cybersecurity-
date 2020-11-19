"""
HOW TO USE jpgLabeler.py:

jpgLabeler.py should be in the directory containing the '00', '01', '02', '03' 
folders and pages.csv. 

When calling the program, you will now be prompled to select a page type from 
the list. The program will iterate over ballots and races for you automatically.
When prompled to enter enter data for a race, you should enter one digit per 
bubble using the dictionary of marks.

Example: In a 3 bubble race, enter labels in the form 001 to indicate that only
the bottom candidate was bubbled in. See 

Instead of entering labels for a race, you can instead type a command:

print: prints the dictionary

open: opens the image

undo: clears the labels for the previous jpg and prompls it to be entered again

stop: saves the data and terminates early. (Use CTRL C to stop without saving)
"""
from PIL import Image
import sys
import os
import csv
import pandas as pd
import numpy as np


def get_image_name(ballot_number):
    top = int(ballot_number / 10000)
    middle = int((ballot_number % 10000) / 100)
    bottom = int(ballot_number % 100)
    image_nm = '0'
    image_nm += str(top) + '/'
    if middle < 10:
        image_nm += '0'
    image_nm += str(middle) + '/'
    if ballot_number < 100000:
        image_nm += '0'
    if ballot_number < 10000:
        image_nm += '0'
    if ballot_number < 1000:
        image_nm += '0'
    if ballot_number < 100:
        image_nm += '0'
    if ballot_number < 10:
        image_nm += '0'
    image_nm += str(ballot_number) + '.jpg'
    return image_nm


pagesdf = pd.read_csv('pages.csv')

dictionary = {'0': 'no mark',
              '1': 'properly bubbled',
              '2': 'X marked',
              '3': 'check marked',
              '4': 'lightly bubbled',
              '5': 'partially bubbled',
              '6': 'bubbled and crossed out',
              '7': 'bad scan / wrong race',
              '8': 'other'}
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

page_types = ['Zachary B. Thoma and Dan Hauser',
              'David R. Couch',
              'Kathleen A. Fairchild',
              'Nicole Chase',
              'Michael Caldwell',
              'Natalie Zall',
              'Sarie Toste Zachary B. Thoma and Dan Hauser',
              'Sherry Dalziel',
              'Kerry Gail Watty',
              'Sarie Toste (left)',
              'Emil Feierabend and Jerry Hansen',
              'Sarie Toste and Dan Hauser',
              'Sarie Toste (right)',
              'Erin Maureen Taylor',
              'Sarie Toste and David R. Couch',
              'Tim Hooven',
              'Tom Chapman',
              'Dan Hauser',
              'John Ash',
              'Gaye Gerdts']

# """"

for i in range(0, len(page_types)):
    print(i, ': ', page_types[i])
choice = int(input('Choose a race number:'))
pl = page_types[choice]


ballotsdf = pd.read_csv('Page Types/' + pl + '/labels.csv')

row = 0
prev = [0]
while row < len(ballotsdf.index):
    labels = ''
    if ballotsdf['Race 0 Bubble 0'][row] == -1:
        nm = get_image_name(ballotsdf['JPGNumber'][row])
        im = Image.open(nm)
        im.show()
        for race_no in range(0, len(page_layout_bubbles[pl])):
            bad_input = 1
            while bad_input == 1:
                bad_input = 0
                labels = input(
                    'Enter Ballot ' + str(ballotsdf['JPGNumber'][row]) + ' Race ' + str(race_no) + ' labels: ')
                if labels == 'stop':
                    break
                elif labels == 'undo':
                    row = prev.pop()
                    for race_no2 in range(0, len(page_layout_bubbles[pl])):
                        for i in range(0, page_layout_bubbles[pl][race_no2]):
                            ballotsdf['Race ' +
                                      str(race_no2) + ' Bubble ' + str(i)][row] = -1
                    break
                elif labels == 'print':
                    bad_input = 1
                    for i in dictionary:
                        print(i, ": ", dictionary[i])
                elif labels == 'open':
                    bad_input = 1
                    im.show()
                elif labels == 'count':
                    bad_input = 1
                    print("Ballots labeled on this run: ", len(prev) - 1)
                    bubbles = 0
                    for i in range(0, len(page_layout_bubbles[pl])):
                        for j in range(0, page_layout_bubbles[pl][i]):
                            bubbles += 1
                    print("Bubbles labeled on this run: ",
                          (len(prev) - 1) * bubbles)
                    ballots = 1
                    for i in range(row, len(ballotsdf.index)):
                        if ballotsdf['Race 0 Bubble 0'][i] == -1:
                            ballots += 1
                    print("Ballots to go: ", ballots)
                    print("Bubbles to go: ", ballots * bubbles)
                elif len(labels) != page_layout_bubbles[pl][race_no]:
                    bad_input = 1
                else:
                    for ch in labels:
                        if ch not in dictionary:
                            bad_input = 1
            if labels == 'stop' or labels == 'undo':
                break
            for i in range(0, page_layout_bubbles[pl][race_no]):
                ballotsdf['Race ' + str(race_no) +
                          ' Bubble ' + str(i)][row] = labels[i]
        im.close()
        if labels != 'stop' and labels != 'undo':
            prev.append(row)
        elif labels == 'stop':
            break
    if labels != 'undo':
        row += 1
        if row == (len(ballotsdf.index)):
            print("Finished labelling page type: ", pl)
ballotsdf.to_csv('Page Types/' + pl + '/labels.csv', index=False)

os.system('python3 summary.py')
"""
import os

os.makedirs('Page Types')

for r in races:
    os.makedirs('Page Types/' + r)
    with open('Page Types/' + r + '/labels.csv', 'w') as csvfile:
      csvwriter = csv.writer(csvfile)

      # writing the fields
      labels = ['JPGNumber']
      for i in range(0, len(page_layout_bubbles[r])):
        for j in range(0, page_layout_bubbles[r][i]):
          labels.append('Page Types ' + str(i) + ' Bubble ' + str(j))
      csvwriter.writerow(labels)

      # writing the data rows
      rdf = pagesdf[pagesdf['PageType'] == r]
      values = np.ones(len(labels)) * (-1)
      for i in rdf['JPGNumber']:
        values[0] = i
        csvwriter.writerow(values.astype(int))

"""
