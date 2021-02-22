import cv2
import numpy as np
#import scipy.misc
#import csv
#import imageio
#import os
from keras.models import load_model
import pandas as pd
from cnn2 import get_f1 
import easygui
from PIL import Image

THRESHOLD = 0.90

page_type_arr = [
    'Tim Hooven',
    'Sarie Toste and David R. Couch',
    'Tom Chapman',
    'Dan Hauser',
    'John Ash',
    'Gaye Gerdts',
    'Erin Maureen Taylor',
    'Sarie Toste (right)',
    'Sarie Toste and Dan Hauser',
    'Emil Feierabend and Jerry Hansen',
    'Sarie Toste (left)',
    'Kerry Gail Watty',
    'Sherry Dalziel',
    'Sarie Toste Zachary B. Thoma and Dan Hauser',
    'Natalie Zall',
    'Michael Caldwell',
    'Nicole Chase',
    'Kathleen A. Fairchild',
    'David R. Couch', 
    'Zachary B. Thoma and Dan Hauser']

page_layout_bubbles = {
    'Zachary B. Thoma and Dan Hauser': [7, 3],
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

prompt1 = 'Enter a race number\n'
prompt1 += '------------------------------------\n'
for i in range(len(page_type_arr)):
    prompt1 += str(i) + ': ' + page_type_arr[i] + '\n'

ptv = int(easygui.enterbox(msg=prompt1))

page_type = page_type_arr[ptv]

pagesdf = pd.read_csv('pages.csv')

jpgs = np.array(pagesdf['JPGNumber'][pagesdf['PageType'] == page_type])

print(len(jpgs))
unparsedarr = pd.read_csv('unparsed_ballots.csv').to_numpy()

jpgs = [i for i in jpgs if i not in unparsedarr]
print(len(jpgs))

X_list = []
for jpg_num in jpgs:
    for race_no in range(len(page_layout_bubbles[page_type])):
        for bubble_no in range(page_layout_bubbles[page_type][race_no]):
            path = 'bubbles_final/' + str(jpg_num).zfill(6) + '_' + str(ptv) + '_' + str(race_no) + '_' + str(bubble_no) + '.jpg'
            X_list.append(cv2.resize(np.array(Image.open(path)), (28, 28)))
            
X = np.array(X_list).reshape(len(X_list), 28, 28, 1)
X = X.astype('float32')
X /= 255
print(X.shape)

#modelpath = easygui.enterbox(msg='Enter model filename', default='cnn2_model_sherry_dalziel')
modelpath = input('Enter model filename (default=cnn2_model_sherry_dalziel): ')

model = load_model(modelpath, custom_objects={'get_f1':get_f1})

pred_probs = model.predict(X)
pred_labels = pred_probs.argmax(axis=-1)

#output_path = easygui.enterbox(msg='Enter output filename', default='output_sherry.csv')
output_path = input('Enter output path: ')
outputdf = pd.read_csv(output_path)

index = 0
for jpg_num in jpgs:
    for race_no in range(len(page_layout_bubbles[page_type])):
        confidence = 1
        bubble_types = set()
        for bubble_no in range(page_layout_bubbles[page_type][race_no]):
            confidence *= pred_probs[index][pred_labels[index]]
            bubble_types.add(pred_labels[index])
            index += 1
        index -= page_layout_bubbles[page_type][race_no]

        #check kick conditions 
        if (confidence < THRESHOLD) or (len(bubble_types) > 2) or (5 in bubble_types) or (6 in bubble_types):
            
            for bubble_no in range(page_layout_bubbles[page_type][race_no]):
                outputdf['CNN'][index] = 2
                index += 1
        else: 
            for bubble_no in range(page_layout_bubbles[page_type][race_no]):
                outputdf['CNN'][index] = int(bool(pred_labels[index]))
                index += 1

outputdf.to_csv(output_path, index=False)


#[JPGNumber   PageType    RaceNum   BubbleNum   ]


print("Done")

















"""
X_data = X_data.astype('float32')
	X_data /= 255

	pred_probs = model.predict(X_data)
	pred_labels = pred_probs.argmax(axis=-1)

	highest = []
	for bubble in pred_probs:
		max_prob = 0
		for bubble_type in bubble:
			if bubble_type > max_prob:
				max_prob = bubble_type
		
		highest.append(max_prob)
	
	total_confidence = 1
	for x in highest:
		total_confidence *= x

"""