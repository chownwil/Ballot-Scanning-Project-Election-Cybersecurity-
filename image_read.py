import glob
import numpy as np
import cv2
import csv

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


reader = csv.reader(open('summary.csv', 'r'))

X = []

completed_pages = []
num_bubbles = 0

for row in reader: 
	if row[1] == "Complete":
		completed_pages.append(str(page_types[row[0]]))
		num_bubbles += int(row[4])

glob_list = []
for page in completed_pages:
	glob_list += glob.glob("bubbles_final/??????_{}_*.jpg".format(page))

glob_list.sort()

# glob_list = sorted(glob.glob("bubbles_final/??????_[{}]_*.jpg".format(','.join(completed_pages))))
for image_path in glob_list:
	image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
	image = cv2.resize(image, (28, 28))
	X.append(image)

count = 0
with open("X0.csv", 'w', newline='') as myfile1, open("X1.csv", 'w', newline='') as myfile2, open("X2.csv", 'w', newline='') as myfile3, open("X3.csv", 'w', newline='') as myfile4:
	wr = csv.writer(myfile1)
	wr2 = csv.writer(myfile2)
	wr3 = csv.writer(myfile3)
	wr4 = csv.writer(myfile4)
	for x in X:
		print(count)
		x1 = x.flatten()
		if count < 20000:
			wr.writerow(x1)
		elif count < 40000:
			wr2.writerow(x1)
		elif count < 60000:
			wr3.writerow(x1)
		else:
			wr4.writerow(x1)
		count += 1