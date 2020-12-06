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

df = pd.read_csv('output_erin.csv')

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
        bad.add(int(i / 7))

    if df['Actual'][i] == df['CNN'][i]:
        cnn_correct += 1
    elif df['CNN'][i] == 2:
        cnn_correct += 1
        cnn_kick += 1

msg = 'Baseline Accuracy:' + str(baseline_correct) + ' / ' + str(good_data) + '\n'
msg += 'Baseline Kick: ' +  str(baseline_kick) + '\n'
msg += 'CNN Accuracy:' +  str(cnn_correct) + ' / ' + str(good_data) + '\n'
msg += 'CNN Kick: ' + str(cnn_kick)
easygui.msgbox(msg)

for i in bad:
    al = ''
    bl = ''
    cl = ''
    for j in range(7):
        al += str(df['Actual'][i * 7 + j])
        bl += str(df['Baseline'][i * 7 + j])
        cl += (df['CNN'][i * 7 + j])
    nm = get_image_name(df['JPGNumber'][i])
    im = Image.open(nm)
    im.show()
    msg2 = nm + '\n' + al + '\n' + bl + '\n' + cl
    if easygui.ynbox(msg2) == False:
        break