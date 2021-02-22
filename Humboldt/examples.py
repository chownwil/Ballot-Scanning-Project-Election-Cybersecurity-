from PIL import Image
import numpy as np
import pandas as pd
import torch
import glob
import os

def get_JPG_num(JPGNumber):
        if JPGNumber < 10:
                return '00000' + str(JPGNumber)
        elif JPGNumber < 100:
                return '0000' + str(JPGNumber)
        elif JPGNumber < 1000:
                return '000' + str(JPGNumber)
        elif JPGNumber < 10000:
                return '00' + str(JPGNumber)
        else:
                return '0' + str(JPGNumber)


def get_im_name(JPGNumber, race, bubble):
        direc = r"bubbles_final"
        pattern1 = get_JPG_num(JPGNumber) + '_?_' + str(race) + '_' + str(bubble) + '.jpg'
        pattern2 = get_JPG_num(JPGNumber) + '_??_' + str(race) + '_' + str(bubble) + '.jpg'
        matches1 = glob.glob(os.path.join(direc, pattern1))
        if len(matches1) > 0:
                return matches1[0]
        else:
                matches2 = glob.glob(os.path.join(direc, pattern2))
                return matches2[0]

output_dict = {'0': 'output_erin.csv', '1': 'output_gaye.csv', '2': 'output_sarie_dan.csv', '3': 'output_sarie_right.csv', '4': 'output_sherry.csv', '5': 'test.csv'}
count = 0
for key, value in output_dict.items():
    print('             ', key, ': ', value)
file = output_dict[str(input('Select an output file from the options above:'))]

output = pd.read_csv(file)

testdf = output[output['CNN'] != 2]
print(len(testdf))
print(testdf.head())

output = output[output['Actual'] != 7]

print('CNN kicked: ', len(output[output['CNN'] == 2]))
print('Baseline kicked: ', len(output[output['Baseline'] == 2]))

examples = output[(output['Actual'] != output['Baseline']) | (output['Actual'] != output['CNN'])]
examples = examples[(examples['Baseline'] != 2) | (examples['CNN'] != 2)]
examples = examples[(examples['Baseline'] != examples['Actual']) | (examples['CNN'] != 2)]
examples = examples[(examples['CNN'] != examples['Actual']) | (examples['Baseline'] != 2)]

both_wrong = examples[(examples['Actual'] != examples['Baseline']) & (examples['Actual'] != examples['CNN']) & (examples['Baseline'] != 2) & (examples['CNN'] != 2)]

baseline_wrong = examples[(examples['Actual'] != examples['Baseline']) & (examples['CNN'] != examples['Baseline'])]

CNN_wrong = examples[(examples['Actual'] != examples['CNN']) & (examples['Baseline'] != examples['CNN'])]

print('Number where both are wrong: ', len(both_wrong))
print('Number where just baseline is wrong: ', len(baseline_wrong))
print('Number where just CNN is wrong: ', len(CNN_wrong))
print('Total Bubbles: ', len(output))
print('-----------------------------')
print('-----------------------------')

dict = {'0': both_wrong, '1': baseline_wrong, '2': CNN_wrong}

print('both_wrong: ', 0)
print('baseline_wrong: ', 1)
print('CNN_wrong: ', 2)
val = input('Enter your value: ')
df = both_wrong
if (val == '1'):
        df = baseline_wrong
elif (val == '2'):
        df = CNN_wrong



print('Opening 1 misclassified bubble at a time.')
print('To open next, press the Enter key.')
print('To end the program, enter any other input.')
check = ''
print(len(df))
for i in range(len(df)):
        if (check == ''):
                print(np.array(df)[i])
                nm = get_im_name(np.array(df['JPGNumber'])[i], np.array(df['RaceNumber'])[i], np.array(df['BubbleNumber'])[i])
                if nm == -1:
                        print('This bubble is not in bubbles_final')
                else:
                        im = Image.open(nm)
                        im.show()
                check = input('Press the Enter key to show more misclassified images:')
        if (check != ''):
                break
print('Finished showing images!')
