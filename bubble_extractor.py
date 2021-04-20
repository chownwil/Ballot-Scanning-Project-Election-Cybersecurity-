import cv2
import matplotlib.pyplot as plt
import math
from scipy import ndimage
import imageio
from PIL import Image
import numpy as np

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


def intersection(top, bottom, left, right):
    d = (top[1] - bottom[1]) * (left[0] - right[0]) - (top[0] - bottom[0]) * (left[1] - right[1])
    if d:
        uA = ((top[0] - bottom[0]) * (right[1] - bottom[1]) - (top[1] - bottom[1]) * (right[0] - bottom[0])) / d
        uB = ((left[0] - right[0]) * (right[1] - bottom[1]) - (left[1] - right[1]) * (right[0] - bottom[0])) / d
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = right[0] + uA * (left[0] - right[0])
    y = right[1] + uA * (left[1] - right[1])
 
    return math.floor(x), math.floor(y)


def centerXCoord(cont):
    return centerFinder(cont)[0]

def centerYCoord(cont):
    return centerFinder(cont)[1]

def baseline(img):
    img = Image.fromarray(img)
    img_gray = img.convert("1")
    pil_bw = np.array(img_gray)
    count = 0
    for r in pil_bw:
        for c in r:
            if c == False:
                count +=1
    return (count/(pil_bw.shape[0]*pil_bw.shape[1])) < 0.07

# 5892


def extract_bubbles(img, image_path, page_num, bubbles_races, races, logging):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
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

    if len(rights) != 63 or len(tops) != 32 or len(bottoms) != 33 or len(lefts) != 63:
        for i in range(min(len(lefts), len(rights))):
            img = cv2.line(img, centerTopPointFinder(lefts[i]), centerTopPointFinder(rights[i]), (0,0,0), 1)
            img = cv2.line(img, centerBottomPointFinder(lefts[i]), centerBottomPointFinder(rights[i]), (0,0,0), 1)

        for i in range(min(len(tops), len(bottoms))):
            img = cv2.line(img, centerRightPointFinder(tops[i]), centerRightPointFinder(bottoms[i]), (0,0,0), 1)
            img = cv2.line(img, centerLeftPointFinder(tops[i]), centerLeftPointFinder(bottoms[i]), (0,0,0), 1)
        imageio.imwrite("bad_ballots/output_lines_{}.jpg".format(image_path),img)
        logging.warning("uh oh could not identify timing marks for image {}".format(image_path))
        return

    """
    Draws Lines
    """
    # for i in range(min(len(lefts), len(rights))):
    #     img = cv2.line(img, centerTopPointFinder(lefts[i]), centerTopPointFinder(rights[i]), (255,0,0), 1)
    #     img = cv2.line(img, centerBottomPointFinder(lefts[i]), centerBottomPointFinder(rights[i]), (255,0,0), 1)

    # for i in range(min(len(tops), len(bottoms))):
    #     img = cv2.line(img, centerRightPointFinder(tops[i]), centerRightPointFinder(bottoms[i]), (255,0,0), 1)
    #     # img = cv2.line(img, centerLeftPointFinder(tops[i]), centerLeftPointFinder(bottoms[i]), (255,0,0), 1)

    # for i in range(min(len(lefts), len(rights))):
    #     for j in range(min(len(tops), len(bottoms))):
    #         if j%2 == 1:
    #             continue
    #         line_intersection = (intersection(centerRightPointFinder(tops[j]), centerRightPointFinder(bottoms[j]), centerFinder(lefts[i]), centerFinder(rights[i])))
    #         img = cv2.rectangle(img, (line_intersection[0]-8, line_intersection[1]-25), (line_intersection[0]+42, line_intersection[1]+25) , color=(0, 255, 0), thickness=1)

    race = 0
    for bubbles in bubbles_races:
        bubble = 0
        for michael in bubbles:
            j, i = michael
            line_intersection = (intersection(centerRightPointFinder(tops[j]), centerRightPointFinder(bottoms[j]), centerFinder(lefts[i]), centerFinder(rights[i])))
            img = cv2.rectangle(img, (line_intersection[0]-8, line_intersection[1]-25), (line_intersection[0]+42, line_intersection[1]+25) , color=(0, 255, 0), thickness=1)
            bubble_extracted = img[line_intersection[1]-25:line_intersection[1]+25,line_intersection[0]-8:line_intersection[0]+42]
            blank = 0 if baseline(bubble_extracted) else 1
            imageio.imwrite('bubbles/{}_{}_{}_{}_{}.jpg'.format(image_path,str(page_num),str(races[race]),str(bubble),str(blank)), bubble_extracted)
            bubble += 1
        race += 1

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


# extract_bubbles(cv2.imread('June ICC ABS/Batch001/Images/00760_00001_000012.tif'), 0, 0,  [ [(0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29)], [(0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], [(0,42)], [(11,18), (11,19)], [(11,23)], [(11,27)], [(11,31)], [(11,34)], [(11,38)], [(11,44), (11,45)], [(22,18), (22,19)], [(22,23), (22,24)], [(22,28), (22,29)], [(22,33), (22,34)], [(22,38), (22,39)] ])


# def findBubbles(filename, bubble_timing)