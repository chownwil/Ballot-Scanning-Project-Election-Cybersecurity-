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

valid_dict = {
                 '0': 'blank page',
                 '1': 'Zachary B. Thoma and Dan Hauser',
                 '2': 'David R. Couch',
                 '3': 'Kathleen A. Fairchild',
                 '4': 'Nicole Chase',
                 '5': 'Michael Caldwell',
                 '6': 'Natalie Zall',
                 '7': 'Sarie Toste Zachary B. Thoma and Dan Hauser',
                 '8': 'Sherry Dalziel',
                 '9': 'Kerry Gail Watty',
                 '10': 'Sarie Toste (left)',
                 '11': 'Emil Feierabend and Jerry Hansen',
                 '12': 'Sarie Toste and Dan Hauser',
                 '13': 'Sarie Toste (right)',
                 '14': 'Erin Maureen Taylor',
                 '15': 'Sarie Toste and David R. Couch',
                 '16': 'Tim Hooven',
                 '17': 'Tom Chapman',
                 '18': 'Dan Hauser',
                 '19': 'John Ash',
                 '20': 'Gaye Gerdts',
                 'open': 'Reopens current JPG',
                 'count': 'Prints info about current run to Terminal',
                 'back': 'Goes back to previous JPG'
    }

ballot_number = 1

prompt = 'Verify Page Layout\n'
prompt += '-------------------------------------\n'
for i in valid_dict:
    prompt += i + ': ' + valid_dict[i] + '\n'

JPGs = []
for i in range(len(pagesdf.index)):
    if pagesdf['PageType'][i] == valid_dict['0']:
        JPGs.append(i)
row = 0
while row < len(JPGs):
    val = None
    nm = get_image_name(pagesdf['JPGNumber'][JPGs[row]])
    im = Image.open(nm)
    im.show()
    bad_input = True
    while bad_input:
        bad_input = False
        val = easygui.enterbox(msg=prompt, default = '0')
        if val == None:
            break
        elif val not in valid_dict:
            bad_input = True
            continue
        elif val == 'open':
            bad_input = True
            im.show()
            continue
        elif val == 'count':
            bad_input = True
            msg = 'JPGs Classified: ' + str(row) + '\n'
            msg += 'JPGs to go: ' + str(len(JPGs) - row) + '\n'
            easygui.msgbox(msg=msg)
        elif val == 'back': 
            row -= 2
            break
        elif val == '0':
            pagesdf['PageType'][JPGs[row]] = 'verified ' + valid_dict[val]
        else:
            pagesdf['PageType'][JPGs[row]] = 'changed ' + valid_dict[val] 
    row += 1
    if val == None:
        break     
pagesdf.to_csv('pages.csv', index=False)