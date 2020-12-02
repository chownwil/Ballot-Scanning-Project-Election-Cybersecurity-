import cv2
from PIL import Image
import numpy 

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



im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite('bw_image.png', im_bw)

im_gray2 = Image.open(filename)
im_gray2 = im_gray2.convert('1')
im_gray2.save('PIL_black_white.png')


pil_bw = numpy.array(im_gray2)

print(im_bw)
print(pil_bw)

count = 0

for r in im_bw:
	for c in r:
		if c == 0:
			count +=1

print("OPEN CV")
print(count - CV2_BORDER_SIZE)
print("Less than 12%: ", str(count - CV2_BORDER_SIZE < TWELVE_PERCENT_THRESHOLD))
print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))
print("")
count1 = 0
for r in pil_bw:
	for c in r:
		if c == False:
			count1 +=1
print("")
print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))
print("")
count1 = 0
for r in pil_bw:
	for c in r:
		if c == False:
			count1 +=1
print("")
print("PIL")
print(count1 - PIL_BORDER_SIZE)
print("Less than 12%: ", str(count1 - PIL_BORDER_SIZE < TWELVE_PERCENT_THRESHOLD))
print("Less than 35%: ", str(count - CV2_BORDER_SIZE < THIRTY_FIVE_PERCENT_THRESHOLD))

