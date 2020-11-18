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
        if pagesdf['PageType'][(10 * (int(ballot / 10))) + start - 1] == label and label != 'unlabeled':
            i = (10 * int(ballot / 10)) + start + 1
            while i < ballot - 1:
                pagesdf['PageType'][i] = label
                i += 2
        im.close()
        if ballot < 35650 and pagesdf['PageType'][(10 * (int(ballot / 10) + 1)) + start - 1] == label and label != 'unlabeled':
            i = ballot + 1
            while i < (10 * (int(ballot / 10) + 1)) + start - 1:
                pagesdf['PageType'][i] = label
                i += 2
    ballot += 2
pagesdf.to_csv('pages.csv', index=False)
"""
with open("pages.csv", 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(['JPGNumber', 'PageType'])

    # writing the data rows
    for i in range(0,35660):
        csvwriter.writerow([i, 'unlabeled'])

"""