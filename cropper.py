# naming convention: jpgnum_pagetype_racenum_bubblenum

import cv2
import numpy as np
import scipy.misc

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
ballotToCrop["Zachary B. Thoma and Dan Hauser"] = [[[11, 304], [11, 381], [11, 455], [12, 530],
         [12, 605], [12, 680], [12, 760]], [[13, 986], [13, 1061], [13, 1136]]]






import cv2
import numpy as np
import scipy.misc

im = cv2.imread('00/00/000001.jpg')
max_skew = 10
# breakpoint()
height, width, _ = im.shape

# Create a grayscale image and denoise it
im_gs = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gs = cv2.fastNlMeansDenoising(im_gs, h=3)

# Create an inverted B&W copy using Otsu (automatic) thresholding
im_bw = cv2.threshold(im_gs, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Detect lines in this image. Parameters here mostly arrived at by trial and error.
lines = cv2.HoughLinesP(
    im_bw, 1, np.pi / 180, 200, minLineLength=width / 12, maxLineGap=width / 150
)

# Collect the angles of these lines (in radians)
angles = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    angles.append(np.arctan2(y2 - y1, x2 - x1))

# If the majority of our lines are vertical, this is probably a landscape image
landscape = np.sum([abs(angle) > np.pi / 4 for angle in angles]) > len(angles) / 2

# Filter the angles to remove outliers based on max_skew
if landscape:
    angles = [
        angle
        for angle in angles
        if np.deg2rad(90 - max_skew) < abs(angle) < np.deg2rad(90 + max_skew)
    ]
else:
    angles = [angle for angle in angles if abs(angle) < np.deg2rad(max_skew)]

if len(angles) < 5:
    # Insufficient data to deskew
    im.show()

# Average the angles to a degree offset
angle_deg = np.rad2deg(np.median(angles))

# If this is landscape image, rotate the entire canvas appropriately
if landscape:
    if angle_deg < 0:
        im_gs = cv2.rotate(im_gs, cv2.ROTATE_90_CLOCKWISE)
        angle_deg += 90
    elif angle_deg > 0:
        im_gs = cv2.rotate(im_gs, cv2.ROTATE_90_COUNTERCLOCKWISE)
        angle_deg -= 90

# Rotate the image by the residual offset
M = cv2.getRotationMatrix2D((width / 2, height / 2), angle_deg, 1)
im_gs = cv2.warpAffine(im_gs, M, (width, height), borderMode=cv2.BORDER_REPLICATE)


# Setting the points for cropped image 
left = 5
top = height // 4
right = 164
bottom = 3 * height // 2
  
# Cropped image of above dimension 
# (It will not change orginal image)
im1 = im_gs[390:430,635:695]

breakpoint()

import imageio; imageio.imwrite('file_name_4.jpg', im1)



