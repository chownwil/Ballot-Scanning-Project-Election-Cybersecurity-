import imageio
import cv2
import numpy as np


font = cv2.FONT_HERSHEY_COMPLEX
img = cv2.imread("00/72/007288.jpg", cv2.IMREAD_GRAYSCALE)

max_skew = 10
height, width = img.shape

# Create a grayscale image and denoise it
im_gs = cv2.fastNlMeansDenoising(img, h=3)

# # Create an inverted B&W copy using Otsu (automatic) thresholding
# im_bw = cv2.threshold(im_gs, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# # Detect lines in this image. Parameters here mostly arrived at by trial and error.
# lines = cv2.HoughLinesP(
#     im_bw, 1, np.pi / 180, 200, minLineLength=width / 12, maxLineGap=width / 150
# )

# # Collect the angles of these lines (in radians)
# angles = []
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     angles.append(np.arctan2(y2 - y1, x2 - x1))

# # If the majority of our lines are vertical, this is probably a landscape image
# landscape = np.sum([abs(angle) > np.pi / 4 for angle in angles]) > len(angles) / 2

# # Filter the angles to remove outliers based on max_skew
# if landscape:
#     angles = [
#         angle
#         for angle in angles
#         if np.deg2rad(90 - max_skew) < abs(angle) < np.deg2rad(90 + max_skew)
#     ]
# else:
#     angles = [angle for angle in angles if abs(angle) < np.deg2rad(max_skew)]

# if len(angles) < 5:
#     # Insufficient data to deskew
#     im.show()

# # Average the angles to a degree offset
# angle_deg = np.rad2deg(np.median(angles))

# # If this is landscape image, rotate the entire canvas appropriately
# if landscape:
#     if angle_deg < 0:
#         im_gs = cv2.rotate(im_gs, cv2.ROTATE_90_CLOCKWISE)
#         angle_deg += 90
#     elif angle_deg > 0:
#         im_gs = cv2.rotate(im_gs, cv2.ROTATE_90_COUNTERCLOCKWISE)
#         angle_deg -= 90

# # Rotate the image by the residual offset
# M = cv2.getRotationMatrix2D((width / 2, height / 2), angle_deg, 1)
# im_gs = cv2.warpAffine(im_gs, M, (width, height), borderMode=cv2.BORDER_REPLICATE)


_, threshold = cv2.threshold(im_gs, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if cv2.contourArea(cnt) < 1500000 or cv2.contourArea(cnt) > 1650000:
        continue
    print(cv2.contourArea(cnt))
    print(approx)
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
imageio.imwrite('shapes.jpg', im_gs[106:, 77:])


"""
Genius Soni Code to Test Pix
1. copy in 3D nested list from cropper.py; fill in bubble coords
2. change im_tl variables to top-left coords of the image
3. uncomment and run
4. use 'c' in pdb to continue (lol I didnt know this, so kept typing 'next' like a noob)
"""
# temp = [ [ [11, 222], [11, 297], [11, 372], [11, 447], [11, 522], [11, 603], [11, 685] ], [ [560, 300], [560, 375], [560, 450], [560, 525], [560, 600], [560, 675], [560, 755] ], [ [560, 979], [560, 1054], [560, 1129] ] ]
# im_tl_x = 105
# im_tl_y = 106
# for race in temp:
#     for t in race:
#         x = t[0]
#         y = t[1]
#         imageio.imwrite('shapes.jpg', im_gs[y+im_tl_y:y+im_tl_y+40, x+im_tl_x:x+im_tl_x+60])
#         breakpoint()
