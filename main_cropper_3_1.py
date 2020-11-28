import cv2
import numpy as np
import scipy.misc
import csv
import imageio
import os

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
ballotToCrop["Tim Hooven"] = [ [ [558, 291], [558, 365], [558, 439], [558, 513], [558, 589], [557, 664], [557, 746], [556, 827] ] ]
ballotToCrop["Sarie Toste and David R. Couch"] = [ [ [12, 220], [13, 296], [13, 370], [13, 446], [13, 521], [13, 601], [14, 683] ], [ [560, 296], [560, 371], [560, 446], [561, 522], [561, 596], [561, 640], [561, 714], [562, 795], [562, 876] ] ]
ballotToCrop["Tom Chapman"] = [ [ [558, 288], [558, 363], [558, 438], [558, 513], [558, 588], [558, 669], [558, 750] ] ]
ballotToCrop["Dan Hauser"] = [ [ [11, 355], [11, 430], [10, 505] ] ]
ballotToCrop["John Ash"] = [ [ [17, 354], [18, 429], [19, 503], [20, 578] ] ]
ballotToCrop["Gaye Gerdts"] = [ [ [557, 320], [557, 396], [557, 471] ] ]
ballotToCrop["Erin Maureen Taylor"] = [ [ [537, 309], [537, 384], [537, 459], [537, 534], [537, 609], [537, 691], [537, 771] ] ]
ballotToCrop["Sarie Toste (right)"] = [ [ [530, 317], [530, 392], [530, 467], [530, 542], [530, 617], [530, 700], [530, 782] ] ]
ballotToCrop["Sarie Toste and Dan Hauser"] = [ [ [6, 228], [6, 303], [6, 378], [6, 453], [6, 528], [6, 608], [6,688] ], [ [554, 357], [554, 423], [554, 512] ] ]
ballotToCrop["Emil Feierabend and Jerry Hansen"] = [ [ [532, 340], [532, 415], [532, 490] ] , [ [532, 688], [532, 763], [532, 808], [532, 883], [532, 958], [532, 1032], [532, 1113], [532, 1193] ] ]
ballotToCrop["Sarie Toste (left)"] = [ [ [8, 225], [8, 300], [8, 375], [8, 450], [8, 525], [8, 607], [8, 698] ] ]
ballotToCrop["Kerry Gail Watty"] = [ [ [533, 369], [533, 444], [533, 519] ] ]
ballotToCrop["Sherry Dalziel"] = [ [ [537, 336], [537, 411], [537, 486], [537, 561], [537, 636], [537, 717], [537, 798] ] ]
ballotToCrop["Sarie Toste Zachary B. Thoma and Dan Hauser"] = [ [ [11, 222], [11, 297], [11, 372], [11, 447], [11, 522], [11, 603], [11, 685] ], [ [560, 300], [560, 375], [560, 450], [560, 525], [560, 600], [560, 675], [560, 755] ], [ [560, 979], [560, 1054], [560, 1129] ] ]
ballotToCrop["Natalie Zall"] = [ [ [562, 285], [562, 360], [562, 435], [562, 510], [562, 585], [562, 660], [562, 742], [562, 824] ] ]
ballotToCrop["Michael Caldwell"] = [ [ [560, 303], [560, 378], [560, 453], [560, 528], [560, 609] ] ]
ballotToCrop["Nicole Chase"] = [ [ [562, 287], [562, 362], [562, 437], [562, 512], [562, 587], [562, 669], [562, 751] ] ]
ballotToCrop["Kathleen A. Fairchild"] = [ [ [560, 314], [560, 389], [560, 464], [560, 539], [560, 615], [560, 695], [560, 777] ] ]
ballotToCrop["David R. Couch"] = [ [ [10, 305], [10, 380], [10, 455], [10, 530], [10, 605], [10, 650], [10, 725], [10, 807], [10, 889] ] ]
ballotToCrop["Zachary B. Thoma and Dan Hauser"] = [[[11, 304], [11, 381], [11, 455], [12, 530], [12, 605], [12, 680], [12, 760]], [[13, 986], [13, 1061], [13, 1136]]]

"""
Requires:  `image` is a valid path to an image
"""
def cropper(image):
	pass

def rect_detect(filepath):
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
	jpg_number = filepath.split('/')[-1][:-4]
	pagetype_name = page_mappings[str(int(jpg_number))]
	try:
		pagetype = page_types[pagetype_name]
    return
	except:
		print("no pagetype: {}".format(pagetype_name))
	bubbles = ballotToCrop[pagetype_name]

	if bounds is None:
		print("Failed to parse ballot: {}".format(jpg_number))
		return
	
	top_left = min(bounds, key=lambda x:sum(x[0]))[0]

	top_left_x = top_left[0]
	top_left_y = top_left[1]

	for i in range(len(bubbles)):
		for j in range(len(bubbles[i])):
			t = bubbles[i][j]
			x=t[0]
			y=t[1]
			imageio.imwrite('bubbles3_1/{}_{}_{}_{}.jpg'.format(jpg_number,pagetype,i,j), im_gs[y+top_left_y:y+top_left_y+40,x+top_left_x:x+top_left_x+60])

def main():
	outside_folders = ['03']
	jpg_number = 30000

	reader = csv.reader(open('pages.csv', 'r'))

	# maps jpg_number to page_type
	for row in reader:
		k, v = row
		page_mappings[k] = v
		
	file1 = open("log_file.txt","w")

	for outside_folder in outside_folders:
		for in_folder in range(14):
			
			inside_folder = str(in_folder)
			inside_folder = inside_folder.zfill(2)

			
			for im_num in range(100):				
				im_num_path = str(jpg_number)
				image_path = im_num_path.zfill(6)
				image_path = outside_folder + '/' + inside_folder + '/' + image_path + '.jpg'

				if os.path.exists(image_path):
					print('sucess', image_path, jpg_number)
					file1.write("{} \n".format(image_path))
					jpg_number += 1
					rect_detect(image_path)
				else:
					print('error:', image_path)
					break

	print('total images scanned:', jpg_number - 1)
	file1.close()

    
    





if __name__=="__main__":
    main()
