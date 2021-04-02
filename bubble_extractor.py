import cv2
import matplotlib.pyplot as plt

def goodPointBottomLeftBlock(cont):
	epsilon = 0.1*cv2.arcLength(cont,True)
	approx = cv2.approxPolyDP(cont,epsilon,True)
	if len(approx) != 4:
		return False
	for point in cont:
		if point[0][0] > 500 or point[0][1] < 2500:
			return False
	return True

def goodPointTopRightBlock(cont):
	epsilon = 0.1*cv2.arcLength(cont,True)
	approx = cv2.approxPolyDP(cont,epsilon,True)
	if len(approx) != 4:
		return False
	for point in cont:
		if point[0][0] < 1500 and point[0][1] > 300:
			return False
	return True

def goodPointLeftSide(cont, bound):
	for point in cont:
		if point[0][0] > bound:
			return False
	return True

def goodPointRightSide(cont, bound):
	for point in cont:
		if point[0][0] < bound:
			return False
	return True

def goodPointTop(cont, bound):
	for point in cont:
		if point[0][1] > bound + 100 or point[0][1] < bound - 100:
			return False
	return True

def goodPointBottom(cont, bound):
	for point in cont:
		if point[0][1] > bound + 100 or point[0][1] < bound - 100:	
			return False
	return True

def centerFinder(cont):
	M = cv2.moments(cont)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	return (cX, cY)

def centerRightPointFinder(cont):
	right_most_point = cont[0][0][0]
	for point in cont:
		if point[0][0] < right_most_point:
			right_most_point = point[0][0]

	M = cv2.moments(cont)
	cY = int(M["m01"] / M["m00"])

	return(right_most_point, cY)


# def centerRightEdgeFinder(cont):
# 	M = cv2.moments(cont)
# 	cX = int(M["m10"] / M["m00"])
# 	cY = int(M["m01"] / M["m00"])
# 	return (cX, cY)

def centerXCoord(cont):
	return centerFinder(cont)[0]

def centerYCoord(cont):
	return centerFinder(cont)[1]

def countContours(filename):
	img = cv2.imread(filename)

	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(imgray, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	bottom_left_block = [cont for cont in contours if cv2.contourArea(cont) > 7500 and cv2.contourArea(cont) < 8500 and goodPointBottomLeftBlock(cont)]
	top_right_block = [cont for cont in contours if cv2.contourArea(cont) > 5500 and cv2.contourArea(cont) < 6500 and goodPointTopRightBlock(cont)]

	# breakpoint()

	top_right_x, top_right_y = centerFinder(top_right_block[0])
	bottom_left_x, bottom_left_y = centerFinder(bottom_left_block[0])




	# return [cv2.contourArea(cont) for cont in top_right_block]

	# approxed_poly = [cv2.approxPolyDP(cont, 0.04* cv2.arcLength(cont, True), True) for cont in contours]


	lefts = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 850 and goodPointLeftSide(cont, bottom_left_x)]
	rights = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 850 and goodPointRightSide(cont, top_right_x)]
	lefts = sorted(lefts, key=centerYCoord)
	rights = sorted(rights, key=centerYCoord)

	tops = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 2000 and goodPointTop(cont, top_right_y)]
	bottoms = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 2000 and goodPointBottom(cont, bottom_left_y)]
	tops = sorted(tops, key=centerXCoord)
	bottoms = sorted(bottoms, key=centerXCoord)




	"""
	Draws Lines
	"""
	for i in range(min(len(lefts), len(rights))):
		img = cv2.line(img, centerFinder(lefts[i]), centerFinder(rights[i]), (255,0,0), 1)

	for i in range(min(len(tops), len(bottoms))):
		img = cv2.line(img, centerRightPointFinder(tops[i]), centerRightPointFinder(bottoms[i]), (255,0,0), 1)

	plt.imsave("output_4.jpg",img)

	"""
	Draws Contours For Debugging
	"""
	# img_2 = cv2.drawContours(img, lefts, -1, (0,255,0), 3)
	# img_2 = cv2.drawContours(img, rights, -1, (0,255,0), 3)
	# img_2 = cv2.drawContours(img, tops, -1, (0,255,0), 3)
	# img_2 = cv2.drawContours(img, bottoms, -1, (0,255,0), 3)

	# breakpoint()

	# img_2 = cv2.drawContours(img, contours, -1, (0,255,0), 3)


	# img_2 = 

	# plt.imsave("contour_out_69.jpg", img_2)

	# plt.imsave("contour_out_69.jpg",cv2.drawContours(img_2, top_right_block, -1, (0,255,0), 3))

	return (len(lefts), len(rights), len(tops), len(bottoms))
	# print(len(rights), len(tops))


	# return (len(rights), len(tops))


countContours('June ICC ABS/Batch001/Images/00760_00001_000001.tif')
