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
import easygui
import time

def get_image_name(ballot_number):
    top = int(ballot_number / 10000)
    middle = int((ballot_number % 10000) / 100)
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

mark_dictionary = {'0': 'no mark',
                   '1': 'properly bubbled',
                   '2': 'X marked',
                   '3': 'check marked',
                   '4': 'lightly bubbled',
                   '5': 'partially bubbled',
                   '6': 'bubbled and crossed out',
                   '8': 'other mark',
                   'open': 'Reopen Image',
                   'undo': 'Undo',
                   'bad': 'bad scan / wrong race'}

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

choice_dictionary = {
    '0': 'Zachary B. Thoma and Dan Hauser',
    '1': 'David R. Couch',
    '2': 'Kathleen A. Fairchild',
    '3': 'Nicole Chase',
    '4': 'Michael Caldwell',
    '5': 'Natalie Zall',
    '6': 'Sarie Toste Zachary B. Thoma and Dan Hauser',
    '7': 'Sherry Dalziel',
    '8': 'Kerry Gail Watty',
    '9': 'Sarie Toste (left)',
    '10': 'Emil Feierabend and Jerry Hansen',
    '11': 'Sarie Toste and Dan Hauser',
    '12': 'Sarie Toste (right)',
    '13': 'Erin Maureen Taylor',
    '14': 'Sarie Toste and David R. Couch',
    '15': 'Tim Hooven',
    '16': 'Tom Chapman',
    '17': 'Dan Hauser',
    '18': 'John Ash',
    '19': 'Gaye Gerdts'}

stop_marks = {2, 3, 4, 5, 6, 8}

# """"
doSleep = easygui.ynbox(msg='Wait to to open enterbox [y/n]? (Yes if using a Mac)')

prompt2 = '-------------------------------------\n'
for i in mark_dictionary:
    prompt2 += i + ': ' + mark_dictionary[i] + '\n'

for pli in choice_dictionary:
    pl = choice_dictionary[pli]
    ballotsdf = pd.read_csv('Page Types/' + pl + '/votes.csv')
    row = 0
    prev = []
    forward = []
    labels = ''
    while row < len(ballotsdf.index):
        islabelled = 1
        for i in range(len(page_layout_bubbles[pl])):
            for j in range(page_layout_bubbles[pl][i]):
                if ballotsdf['Race ' + str(i) + ' Bubble ' + str(j)][row] in stop_marks:
                    islabelled = 0
                    break
            if islabelled == 0:
                break
        if (islabelled == 0) or (row in forward):
            nm = get_image_name(ballotsdf['JPGNumber'][row])
            im = Image.open(nm)
            im.show()
            
            if doSleep:
                time.sleep(1)
            
            for race_no in range(len(page_layout_bubbles[pl])):
                bad_input = 1
                while bad_input == 1:
                    bad_input = 0
                    default = ''
                    for i in range(page_layout_bubbles[pl][race_no]):
                        if ballotsdf['Race ' + str(race_no) + ' Bubble ' + str(i)][row] in stop_marks:
                            default += '1'
                        else:
                            default += str(ballotsdf['Race ' + str(race_no) + ' Bubble ' + str(i)][row])
                    labels = easygui.enterbox(msg='Enter Ballot ' + str(ballotsdf['JPGNumber'][row]) + ' Race ' + str(
                        race_no) + ' labels:\n' + prompt2, default=default)
                    if labels == None:
                        break
                    elif labels == 'undo':
                        forward.append(row)
                        row = prev.pop()
                        break
                    elif labels == 'open':
                        bad_input = 1
                        im.show()
                    elif labels == 'bad':
                        for race_no2 in range(0,len(page_layout_bubbles[pl])):
                            for bubble in range(0,page_layout_bubbles[pl][race_no2]):
                                ballotsdf['Race ' + str(race_no2) + ' Bubble ' + str(bubble)][row] = '7'
                    elif len(labels) != page_layout_bubbles[pl][race_no]:
                        bad_input = 1
                    else:
                        for ch in labels:
                            if (ch != '0') and (ch != '1') and ('ch' != '7'):
                                bad_input = 1
                if labels == None or labels == 'undo' or labels == 'bad':
                    break
                for i in range(0, page_layout_bubbles[pl][race_no]):
                    ballotsdf['Race ' + str(race_no) +
                            ' Bubble ' + str(i)][row] = labels[i]
                labels = ''
            im.close()
            if labels == None:
                break
            if labels == 'undo':
                continue
            prev.append(row)
        row += 1
        if row == (len(ballotsdf.index)):
            easygui.msgbox(msg='Finished labelling page type: ' + pl)
    ballotsdf.to_csv('Page Types/' + pl + '/votes.csv', index=False)
"""
import os

os.makedirs('Page Types')

pagesdf = pd.read_csv('pages.csv')

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
