# load ballot

# identify bubbles and extract them

# load model

# run bubbles through the model

# apply heuristics to classify race based on model


import cv2
import numpy as np
import scipy.misc
import csv
import imageio
import os
from keras.models import load_model



page_mappings = {}

page_types = {}
page_types['Tim Hooven'] = 0
page_types['Sarie Toste and David R. Couch'] = 1
page_types['Tom Chapman'] = 2
page_types['Dan Hauser'] = 3
page_types['John Ash'] = 4
page_types['Gaye Gerdts'] = 5
page_types['Erin Maureen Taylor'] = 6
page_types['Sarie Toste (right)'] = 7
page_types['Sarie Toste and Dan Hauser'] = 8
page_types['Emil Feierabend and Jerry Hansen'] = 9
page_types['Sarie Toste (left)'] = 10
page_types['Kerry Gail Watty'] = 11
page_types['Sherry Dalziel'] = 12
page_types['Sarie Toste Zachary B. Thoma and Dan Hauser'] = 13
page_types['Natalie Zall'] = 14
page_types['Michael Caldwell'] = 15
page_types['Nicole Chase'] = 16
page_types['Kathleen A. Fairchild'] = 17
page_types['David R. Couch'] = 18
page_types['Zachary B. Thoma and Dan Hauser'] = 19

ballotToCrop = {}
# offset from the top left for each bubble in the format: [left_x, top_y]
ballotToCrop["Sherry Dalziel"] = [ [ [558, 315], [558, 390], [558, 465], [558, 540], [558, 615], [558, 697], [558, 779] ] ]

model = load_model('cnn2_model_sherry_dalziel')

# 7 x 28 x 28 x 1
def classifier(bubbles):
	X = [np.reshape(x, (28,28,1)) for x in bubbles]
	X_data = np.array(X)

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

	breakpoint()


def rect_detect(filepath):
	# jpg_number = filepath.split('/')[-1][:-4]
	# pagetype_name = page_mappings[str(int(jpg_number))]
	# if pagetype_name not in ["Sherry Dalziel"]:
	# 	print("Wrong Race! Ballot:", filepath)
	# 	return
	
	bubbles = ballotToCrop["Sherry Dalziel"]

	font = cv2.FONT_HERSHEY_COMPLEX
	img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

	max_skew = 10
	height, width = img.shape

	# Create a grayscale image and denoise it
	im_gs = cv2.fastNlMeansDenoising(img, h=3)

	_, threshold = cv2.threshold(im_gs, 240, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	bounds = None
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
		cv2.drawContours(img, [approx], 0, (0), 5)
		x = approx.ravel()[0]
		y = approx.ravel()[1]
		if cv2.contourArea(cnt) < 1500000 or cv2.contourArea(cnt) > 1650000:
			continue
		bounds = approx
		if len(approx) == 3:
			cv2.putText(im_gs, "Triangle", (x, y), font, 0.5, (0, 0, 255))
		elif len(approx) == 4:
			cv2.putText(im_gs, "Rectangle", (x, y), font, 0.5, (0, 0, 255))
		elif len(approx) == 5:
			cv2.putText(im_gs, "Pentagon", (x, y), font, 0.5, (0, 0, 255))
		elif 6 < len(approx) < 15:
			cv2.putText(im_gs, "Ellipse", (x, y), font, 0.5, (0, 0, 255))
		else:
			cv2.putText(im_gs, "Circle", (x, y), font, 0.5, (0, 0, 255))

	# jpgnum_pagetype_racenum_bubblenum

	if bounds is None:
		print("Failed to parse ballot: {}".format(jpg_number))
		return
	
	top_left = min(bounds, key=lambda x:sum(x[0]))[0]

	top_left_x = top_left[0]
	top_left_y = top_left[1]

	bubbles_to_classify = []

	for i in range(len(bubbles)):
		for j in range(len(bubbles[i])):
			t = bubbles[i][j]
			x=t[0]
			y=t[1]
			bubble = im_gs[y+top_left_y:y+top_left_y+40,x+top_left_x:x+top_left_x+60]
			bubble = cv2.resize(bubble, (28, 28))
			bubbles_to_classify.append(bubble)

	all_bubbles = np.stack(bubbles_to_classify)
	all_bubbles = np.reshape(all_bubbles, (7, 28, 28, 1))
	return all_bubbles


def main():
	image_path = '03/12/031291.jpg'
	if os.path.exists(image_path):
		bubbles = rect_detect(image_path)
		classifier(bubbles)


	# outside_folders = ['00', '01', '02', '03']
	# jpg_number = 1

	# reader = csv.reader(open('pages.csv', 'r'))

	# # maps jpg_number to page_type
	# for row in reader:
	# 	k, v = row
	# 	page_mappings[k] = v
		
	# file1 = open("log_file.txt","w")

	# for outside_folder in outside_folders:
	# 	for in_folder in range(100):
			
	# 		inside_folder = str(in_folder)
	# 		inside_folder = inside_folder.zfill(2)

			
	# 		for im_num in range(100):				
	# 			im_num_path = str(jpg_number)
	# 			image_path = im_num_path.zfill(6)
	# 			image_path = outside_folder + '/' + inside_folder + '/' + image_path + '.jpg'

	# 			if os.path.exists(image_path):
	# 				print('sucess', image_path, jpg_number)
	# 				file1.write("{} \n".format(image_path))
	# 				jpg_number += 1
	# 				rect_detect(image_path)
	# 			else:
	# 				print('error:', image_path)
	# 				break

	# print('total images scanned:', jpg_number - 1)
	# file1.close()


	





if __name__=="__main__":
	main()
