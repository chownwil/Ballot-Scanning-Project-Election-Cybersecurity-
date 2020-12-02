import imageio
import cv2
import numpy as np


font = cv2.FONT_HERSHEY_COMPLEX
img = cv2.imread("00/33/003354.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.imread("005924_1_0_5.jpg", cv2.IMREAD_GRAYSCALE)


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
    print(cv2.contourArea(cnt))
    print(approx)
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
breakpoint()
import imageio; imageio.imwrite('shapes_1.jpg', im_gs[:,:])


# I'm using the code below to test the bubble positions. Replace 103 and 105 with rectangle positions for this ballot

# race = [ [ [10, 225] , [10, 300], [10, 375], [10, 450], [12, 525], [12, 600], [12, 675] ], [ [554, 357], [554, 423], [554, 512] ] ]
race = [ [ [10, 354], [10, 429], [10, 503], [10, 578] ] ]
top_left = min(bounds, key=lambda x:sum(x[0]))[0]

top_left_x = top_left[0]
top_left_y = top_left[1]

for r in race:
    for t in r:
        x=t[0];y=t[1];import imageio; imageio.imwrite('shapes.jpg', im_gs[y+top_left_y:y+top_left_y+40,x+top_left_x:x+top_left_x+60])
        print(x,y)
        breakpoint()
    print('next race')
