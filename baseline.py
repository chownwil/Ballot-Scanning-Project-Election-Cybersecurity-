import cv2
from PIL import Image
import numpy 
import glob 
import csv 

CV2_BORDER_SIZE = 705
PIL_BORDER_SIZE = 604

BUBBLE_AREA = 646

TWELVE_PERCENT_THRESHOLD = 78 

THIRTY_FIVE_PERCENT_THRESHOLD = 226

# sample X bubble
# filename = "bubbles_final/013671_11_0_1.jpg"

#sample X bubble 2
# filename = "bubbles_final/013669_11_0_1.jpg"

#sample X bubble 3
# filename = "bubbles_final/013953_0_0_1.jpg"

#sample X bubble 4
filename = "bubbles_final/014081_0_0_3.jpg"

glob_list = glob.glob("bubbles_final/??????_12_*.jpg")

unsure_ballots = set()

output = []

for image_path in sorted(glob_list):
	im_gray2 = Image.open(image_path)
	im_gray2 = im_gray2.convert('1')
	pil_bw = numpy.array(im_gray2)
	count1 = 0
	for r in pil_bw:
		for c in r:
			if c == False:
				count1 +=1
	print(image_path)
	jpg, pagetype, race_index, bubble_index = image_path[14:-4].split('_')
	predicted = 1
	# print(count1 - PIL_BORDER_SIZE)
	if count1 - PIL_BORDER_SIZE < TWELVE_PERCENT_THRESHOLD:
		predicted = 0
	elif count1 - PIL_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD:
		unsure_ballots.add(jpg)
		predicted = 2
	output.append([jpg,race_index,bubble_index,-1,predicted,-1])

with open("output.csv", 'w', newline='') as myfile:
	wr = csv.writer(myfile)
	for i in range(len(output)):
		if output[i][0] in unsure_ballots:
			output[i][4] = 2
		wr.writerow(output[i])

with open("unsure_ballots_baseline", 'w', newline='') as myfile:
	myfile.write(str(unsure_ballots))

print(unsure_ballots)

# im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
# (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imwrite('bw_image.png', im_bw)




# pil_bw = numpy.array(im_gray2)

# print(im_bw)
# print(pil_bw)

# count = 0

# for r in im_bw:
# 	for c in r:
# 		if c == 0:
# 			count +=1

# print("OPEN CV")
# print(count - CV2_BORDER_SIZE)
# print("Less than 12%: ", str(count - CV2_BORDER_SIZE < TWELVE_PERCENT_THRESHOLD))
# print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))
# print("")
# count1 = 0
# for r in pil_bw:
# 	for c in r:
# 		if c == False:
# 			count1 +=1
# print("")
# print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))
# print("")
# count1 = 0
# for r in pil_bw:
# 	for c in r:
# 		if c == False:
# 			count1 +=1
# print("")
# print("PIL")
# print(count1 - PIL_BORDER_SIZE)
# print("Less than 12%: ", str(count1 - PIL_BORDER_SIZE < TWELVE_PERCENT_THRESHOLD))
# print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))

