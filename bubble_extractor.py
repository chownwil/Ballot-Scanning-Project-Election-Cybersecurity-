import cv2
import matplotlib.pyplot as plt
import math
from scipy import ndimage

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

def centerLeftPointFinder(cont):
    left_most_point = cont[0][0][0]
    for point in cont:
        if point[0][0] > left_most_point:
            left_most_point = point[0][0]

    M = cv2.moments(cont)
    cY = int(M["m01"] / M["m00"])

    return(left_most_point, cY)

def centerTopPointFinder(cont):
    top_most_point = cont[0][0][1]
    for point in cont:
        if point[0][1] < top_most_point:
            top_most_point = point[0][1]

    M = cv2.moments(cont)
    cX = int(M["m10"] / M["m00"])

    return(cX, top_most_point)

def centerBottomPointFinder(cont):
    bottom_most_point = cont[0][0][1]
    for point in cont:
        if point[0][1] > bottom_most_point:
            bottom_most_point = point[0][1]

    M = cv2.moments(cont)
    cX = int(M["m10"] / M["m00"])

    return(cX, bottom_most_point)


# def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
def intersection(top, bottom, left, right):
    # d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    d = (top[1] - bottom[1]) * (left[0] - right[0]) - (top[0] - bottom[0]) * (left[1] - right[1])
    if d:
        # uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uA = ((top[0] - bottom[0]) * (right[1] - bottom[1]) - (top[1] - bottom[1]) * (right[0] - bottom[0])) / d
        # uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        uB = ((left[0] - right[0]) * (right[1] - bottom[1]) - (left[1] - right[1]) * (right[0] - bottom[0])) / d
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    # x = Ax1 + uA * (Ax2 - Ax1)
    x = right[0] + uA * (left[0] - right[0])
    # y = Ay1 + uA * (Ay2 - Ay1)
    y = right[1] + uA * (left[1] - right[1])
 
    return math.floor(x), math.floor(y)


def centerXCoord(cont):
    return centerFinder(cont)[0]

def centerYCoord(cont):
    return centerFinder(cont)[1]

def countContours(filename):
    img = cv2.imread(filename)

    # img = ndimage.rotate(img, 5)

    # plt.imsave("output_lines.jpg",img)

    # return

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bottom_left_block = [cont for cont in contours if cv2.contourArea(cont) > 7500 and cv2.contourArea(cont) < 8500 and goodPointBottomLeftBlock(cont)]
    top_right_block = [cont for cont in contours if cv2.contourArea(cont) > 5500 and cv2.contourArea(cont) < 6500 and goodPointTopRightBlock(cont)]

    top_right_x, top_right_y = centerFinder(top_right_block[0])
    bottom_left_x, bottom_left_y = centerFinder(bottom_left_block[0])

    lefts = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 850 and goodPointLeftSide(cont, bottom_left_x)]
    rights = [cont for cont in contours if cv2.contourArea(cont) > 650 and cv2.contourArea(cont) < 850 and goodPointRightSide(cont, top_right_x)]
    lefts = sorted(lefts, key=centerYCoord)
    rights = sorted(rights, key=centerYCoord)

    tops = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 2000 and goodPointTop(cont, top_right_y)]
    bottoms = [cont for cont in contours if cv2.contourArea(cont) > 1450 and cv2.contourArea(cont) < 2000 and goodPointBottom(cont, bottom_left_y)]
    tops = sorted(tops, key=centerXCoord)
    bottoms = sorted(bottoms, key=centerXCoord)

    len(lefts), len(rights), len(tops), len(bottoms)

    if len(rights) != 47 or len(tops) != 32 or len(bottoms) != 33 or len(lefts) != 47:
        breakpoint()
        print("uh oh")

    """
    Draws Lines
    """
    # for i in range(min(len(lefts), len(rights))):
    #     img = cv2.line(img, centerTopPointFinder(lefts[i]), centerTopPointFinder(rights[i]), (255,0,0), 1)
    #     img = cv2.line(img, centerBottomPointFinder(lefts[i]), centerBottomPointFinder(rights[i]), (255,0,0), 1)

    # for i in range(min(len(tops), len(bottoms))):
    #     img = cv2.line(img, centerRightPointFinder(tops[i]), centerRightPointFinder(bottoms[i]), (255,0,0), 1)
    #     # img = cv2.line(img, centerLeftPointFinder(tops[i]), centerLeftPointFinder(bottoms[i]), (255,0,0), 1)

    for i in range(min(len(lefts), len(rights))):
        for j in range(min(len(tops), len(bottoms))):
            if j%2 == 1:
                continue
            line_intersection = (intersection(centerRightPointFinder(tops[j]), centerRightPointFinder(bottoms[j]), centerFinder(lefts[i]), centerFinder(rights[i])))
            img = cv2.rectangle(img, (line_intersection[0]-8, line_intersection[1]-25), (line_intersection[0]+42, line_intersection[1]+25) , color=(0, 255, 0), thickness=1)

    plt.imsave("output_lines.jpg",img)

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


countContours('June ICC ABS/Batch001/Images/00760_00001_000012.tif')


# def findBubbles(filename, bubble_timing)