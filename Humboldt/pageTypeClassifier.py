from PIL import Image
import sys
import csv
import pandas as pd
import numpy as np

"""
This program can be used to classify the .jpg scans by the layout on the page. 
This program makes some assumptions about nearby even and odd ballots and may not classify all images with 100% accuracy

Run in Terminal or CommandPrompt. 
Call using `python3 pageTypeClassifier.py iterate_odd_ballot_nums step_size previous_step_size`

Special Commands while running
    print: prints a table of already defined inputs and thier hotkey tags 
    (note: tags are not necessarily consistent over runs so always check when you start)
    open: Reopens the current image in case it didn't open correctly the first time
    stop: save and terminates the program

To add a new type of page simply type it and you will be asked to define a temporary tag for it

Note: If you make a mistake classifying a page type, call stop immediately and manually fix pages.csv 
(note nearby unlabeled data may have been effected by a bad label)
"""

def get_image_name(ballot_number):
    ballot_number = ballot_number
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


start = int(sys.argv[1])
step = int(sys.argv[2])
prev_step = int(sys.argv[3])

pagesdf = pd.read_csv('pages.csv')

valid = {'-1': 'unlabeled', '0': 'blank page'}
valid_set = {'unlabeled', 'blank page'}
index = 1
count = 0
for label in pagesdf['PageType']:
    if label not in valid_set:
        valid_set.add(label)
        valid[str(index)] = label
        index += 1
    if label == 'unlabeled':
        count += 1
print(count)
ballot = start
while ballot < 35660:
    if pagesdf['PageType'][ballot - 1] == 'unlabeled':
        nm = get_image_name(ballot)
        im = Image.open(nm)
        im.show()
        label = 'unlabeled'
        while label == 'unlabeled':
            string = input('Enter data for ballot ' + str(ballot) + ': ')
            if string == 'stop':
                break
            elif string == 'print':
                for tag in valid:
                    print(tag, ": ", valid[tag])
            elif string == 'open':
                im.show()
            elif string in valid:
                label = valid[string]
            elif input('Add ' + string + ' to tags dict [y/n]:') == 'y':
                temp = input('Enter tag definition:')
                if input('Confirm [y/n]:') == 'y':
                    label = temp
                    valid[string] = label
        if string == 'stop':
            break
        pagesdf['PageType'][ballot - 1] = label
        if pagesdf['PageType'][(prev_step * (int(ballot / prev_step))) + start - 1] == label and label != 'unlabeled':
            i = (prev_step * int(ballot / prev_step)) + start + 1
            while i < ballot - 1:
                pagesdf['PageType'][i] = label
                i += 2
        im.close()
        if ballot < 35650 and pagesdf['PageType'][(prev_step * (int(ballot / prev_step) + 1)) + start - 1] == label and label != 'unlabeled':
            i = ballot + 1
            while i < (prev_step * (int(ballot / prev_step) + 1)) + start - 1:
                pagesdf['PageType'][i] = label
                i += 2
    ballot += step
pagesdf.to_csv('pages.csv', index=False)
"""
#initializer code for pages.csv
with open("pages.csv", 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(['JPGNumber', 'PageType'])

    # writing the data rows
    for i in range(0,35660):
        csvwriter.writerow([i, 'unlabeled'])

"""
