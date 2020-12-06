import pandas as pd 
import numpy as np
from PIL import Image
import easygui

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

filename = easygui.enterbox(msg='Enter Filename:')

baseline_correct = 0
cnn_correct = 0

baseline_kick = 0
cnn_kick = 0
good_data = 0

bad = set()

for i in range(len(df)):
    if df['Actual'][i] == 7:
        continue
    good_data += 1
    if df['Actual'][i] == df['Baseline'][i]:
        baseline_correct += 1
    elif df['Baseline'][i] == 2:
        baseline_correct += 1
        baseline_kick += 1
    else:
        bad.add(df['JPGNumber'][i])
    if df['Actual'][i] == df['CNN'][i]:
        cnn_correct += 1
    elif df['CNN'][i] == 2:
        cnn_correct += 1
        cnn_kick += 1
    else:
        bad.add(df['JPGNumber'][i])

msg = 'Baseline Accuracy:' + str(baseline_correct) + ' / ' + str(good_data) + '\n'
msg += 'Baseline Kick: ' +  str(baseline_kick) + '\n'
msg += 'CNN Accuracy:' +  str(cnn_correct) + ' / ' + str(good_data) + '\n'
msg += 'CNN Kick: ' + str(cnn_kick)
easygui.msgbox(msg)

for i in bad:
    im = Image.open(get_image_name(i))
    im.show()
    msg = 'Actual: '
    for j in df[df['JPGNumber'] == i]['Actual'].to_numpy().flatten():
        msg += str(j)
    msg += '\n'
    msg += 'Baseline: '
    for j in df[df['JPGNumber'] == i]['Baseline'].to_numpy().flatten():
        msg += str(j)
    msg += '\n'
    msg += 'CNN: '
    for j in df[df['JPGNumber'] == i]['CNN'].to_numpy().flatten():
        msg += str(j)
    msg += '\n'
    if easygui.ynbox(msg) == False:
        break
