import glob
import csv
import bubble_extractor
import cv2
from PIL import Image
import imageio
import numpy as np
import logging

logging.root.setLevel(logging.NOTSET)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.basicConfig(filename="bubbles.log", filemode='w+', format='%(name)s - %(levelname)s - %(message)s')


glob_list = glob.glob("Pueblo/Project ICC 101/Batch???/Images/*.tif")

pagetype_bubble_mapping = {
    0: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,15), (28,15)]
		]
	],
    1: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], [(22,22), (22,23), (22,24)], 
			[(22,28)], [(22,32), (22,33)], [(22,36)], 
			[(22,42), (28,42)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,53), (28,53)], 
			[(22,57), (28,57)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)], 
			[(22,59), (28,59)]
		]
	],
    2: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23), (22,24)], 
			[(22,28)], 
			[(22,32), (22,33)], 
			[(22,36)], 
			[(22,42), (28,42)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,53), (28,53)], 
			[(22,57), (28,57)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,15), (28,15)]
		]
	],
    3: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)],
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)], 
			[(22,59), (28,59)]
		]
	],
    4: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,15), (28,15)]
		]
	],
    5: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)]
		]
	],
    6: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,26), (22,27)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,39)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,53), (28,53)], 
			[(22,56), (28,56)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,7), (6,7)], 
			[(0,24), (6,24)],
			[(0,30), (6,30)], 
			[(0,34), (6,34)], 
			[(0,41), (6,41)], 
			[(0,57), (6,57)], 
			[(0,62), (6,62)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)]
		]
	],
    7: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,26), (22,27)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,39)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,53), (28,53)], 
			[(22,56), (28,56)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,7), (6,7)], 
			[(0,24), (6,24)], 
			[(0,30), (6,30)], 
			[(0,34), (6,34)], 
			[(0,41), (6,41)], 
			[(0,57), (6,57)], 
			[(0,62), (6,62)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)]
		]
	],
    8: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,26), (22,27), (22,28)], 
			[(22,32)], 
			[(22,36), (22,37)], 
			[(22,40)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,54), (28,54)], 
			[(22,57), (28,57)], 
			[(22,61), (28,61)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,7), (6,7)], 
			[(0,24), (6,24)], 
			[(0,30), (6,30)], 
			[(0,34), (6,34)], 
			[(0,41), (6,41)], 
			[(0,57), (6,57)], 
			[(0,62), (6,62)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)]
		]
	],
    9: [
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(22,35), (28,35)]
		]
	],
    10: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)]
		]
	],
    11: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,15), (28,15)], 
			[(22,51), (28,51)]
		]
	],
    12: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,26), (22,27)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,39)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,53), (28,53)], 
			[(22,56), (28,56)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,7), (6,7)], 
			[(0,24), (6,24)], 
			[(0,30), (6,30)], 
			[(0,34), (6,34)], 
			[(0,41), (6,41)], 
			[(0,57), (6,57)], 
			[(0,62), (6,62)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)]
		]
	],
    13: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,26), (22,27), (22,28)], 
			[(22,32)], 
			[(22,36), (22,37)], 
			[(22,40)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,54), (28,54)], 
			[(22,57), (28,57)], 
			[(22,61), (28,61)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,7), (6,7)], 
			[(0,24), (6,24)], 
			[(0,30), (6,30)], 
			[(0,34), (6,34)], 
			[(0,41), (6,41)], 
			[(0,57), (6,57)], 
			[(0,62), (6,62)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)]
		]
	],
    14: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23), (22,24)], 
			[(22,28)], 
			[(22,32), (22,33)], 
			[(22,36)], 
			[(22,42), (28,42)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,53), (28,53)], 
			[(22,57), (28,57)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)], 
			[(22,35), (28,35)]
		]
	],
    15: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23)], 
			[(22,31)], 
			[(22,35), (22,36)], 
			[(22,41), (28,41)], 
			[(22,45), (28,45)], 
			[(22,49), (28,49)], 
			[(22,52), (28,52)], 
			[(22,56), (28,56)], 
			[(22,59), (28,59)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], 
			[(11,23), (17,23)], 
			[(11,30), (17,30)], 
			[(11,47), (17,47)]
		]
	],
    16: 
	[
		[
			[(0,17), (0,18), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24), (0,25), (0,26), (0,27), (0,28), (0,29), (0,30), (0,31), (0,32), (0,33), (0,34), (0,35), (0,36), (0,37), (0,38)], 
			[(0,41), (0,42), (0,43), (0,44), (0,45), (0,46)], 
			[(0, 49), (0,50), (0,51), (0,52)], 
			[(22, 18), (22, 19)], 
			[(22,22), (22,23), (22,24)], 
			[(22,28)], 
			[(22,32), (22,33)], 
			[(22,36)], 
			[(22,42), (28,42)], 
			[(22,46), (28,46)], 
			[(22,50), (28,50)], 
			[(22,53), (28,53)], 
			[(22,57), (28,57)], 
			[(22,60), (28,60)]
		], 
		[
			[(0,3), (6,3)], 
			[(0,20), (6,20)], 
			[(0,26), (6,26)], 
			[(0,30), (6,30)], 
			[(0,37), (6,37)], 
			[(0,53), (6,53)], 
			[(0,58), (6,58)], 
			[(11, 8), (17,8)], 
			[(11,19), (17,19)], [(11,23), (17,23)], [(11,30), (17,30)], [(11,47), (17,47)]
		]
	]
}

pagetype_race_mapping = []

with open('pueblo_page_type_keys.csv', newline='') as csvfile:
	for row in csv.reader(csvfile):
		row = row[:-1]
		row_int = [int(elem) for elem in row]
		pagetype_race_mapping.append(row_int)

image_pagetype_mapping = {}

with open('pueblo_page_types.csv', newline='') as csvfile:
	for row in csv.reader(csvfile):
		img_name = row[0].split(".")[0][1:-8]
		image_pagetype_mapping[img_name] = int(row[1])

prev_batch_name = None

for glob in sorted(glob_list):
	try:
		img = Image.open(glob)
		image_path = glob.split("/")[-1].split(".")[0]
		batch_name = image_path.split("_")[1]
		if batch_name != prev_batch_name:
			if prev_batch_name != None:
				logging.info("Done processing {}".format(prev_batch_name))
			prev_batch_name = batch_name
		pagetype = image_pagetype_mapping[image_path]
		if pagetype not in pagetype_bubble_mapping:
			logging.warning("missing pagetype: ", pagetype, " for ballot ", glob)
			continue
		bubble_extractor.extract_bubbles(np.array(img).astype(np.uint8)*255, image_path, 0, pagetype_bubble_mapping[pagetype][0], pagetype_race_mapping[pagetype][0:len(pagetype_bubble_mapping[pagetype][0])], logging)
		img.seek(1)
		bubble_extractor.extract_bubbles(np.array(img).astype(np.uint8)*255, image_path, 1, pagetype_bubble_mapping[pagetype][1], pagetype_race_mapping[pagetype][len(pagetype_bubble_mapping[pagetype][0]):], logging)
	except:
		logging.warning("error processing ballot ", glob)