import cv2
import matplotlib.pyplot as plt

def goodPointLeftSide(cont):
	for point in cont:
		if point[0][0] > 100:
			return False
	return True

def goodPointRightSide(cont):
	for point in cont:
		if point[0][0] < 1630:
			return False
	return True

def goodPointTop(cont):
	for point in cont:
		if point[0][1] > 200:
			return False
	return True

def goodPointBottom(cont):
	for point in cont:
		if point[0][1] < 2680:
			return False
	return True

def centerFinder(cont):
	M = cv2.moments(cont)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	return (cX, cY)

def centerXCoord(cont):
	return centerFinder(cont)[0]

def centerYCoord(cont):
	return centerFinder(cont)[1]


img = cv2.imread('June ICC ABS/Batch001/Images/00760_00001_000002.tif')
plt.imshow(img)

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# approxed_poly = [cv2.approxPolyDP(cont, 0.04* cv2.arcLength(cont, True), True) for cont in contours]
# breakpoint()
lefts = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 800 and goodPointLeftSide(cont)]
rights = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 800 and goodPointRightSide(cont)]
lefts = sorted(lefts, key=centerYCoord)
rights = sorted(rights, key=centeryCoord)

tops = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 1600 and goodPointTop(cont)]
bottoms = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 1600 and goodPointBottom(cont)]
tops = sorted(tops, key=centerXCoord)
bottoms = sorted(bottoms, key=centerXCoord)

# breakpoint()

for i in range(len(lefts)):
	img = cv2.line(img, centerFinder(lefts[i]), centerFinder(rights[i]), (255,0,0), 1)

for i in range(len(tops)):
	img = cv2.line(img, centerFinder(tops[i]), centerFinder(bottoms[i]), (255,0,0), 1)

plt.imsave("output.jpg",img)
# breakpoint()
# wanted_rectangles = [cont for cont in contours if (cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 800 and goodPointSide(cont)) or (cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 1600 and goodPointBottop(cont))]
# img_2 = cv2.drawContours(img, wanted_rectangles, -1, (0,255,0), 3)
# # breakpoint()
# plt.imsave("output.jpg",img_2)


# img_2 = cv2.drawContours(img, wanted_rectangles, -1, (0,255,0), 3); plt.imsave("output.jpg",img_2)