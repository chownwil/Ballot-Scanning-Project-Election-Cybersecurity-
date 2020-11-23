import cv2
import numpy as np
import scipy.misc
import csv


page_types = {}
page_types['Tim Hooven'] = 0
page_types['Sarie Toste and David R. Couch'] = 1
page_types['Tom Chapman'] = 2
page_types['Dan Hauser'] = 3
page_types['John Ash'] = 4
page_types['Gaye Gerdts'] = 5
page_types['Erin Maureen Taylor'] = 6
page_types['Sarie Toste (right)'] = 7
page_types['Sarie Toste and Dan Hauser'] = 8
page_types['Emil Feierabend and Jerry Hansen'] = 9
page_types['Sarie Toste (left)'] = 10
page_types['Kerry Gail Watty'] = 11
page_types['Sherry Dalziel'] = 12
page_types['Sarie Toste Zachary B. Thoma and Dan Hauser'] = 13
page_types['Natalie Zall'] = 14
page_types['Michael Caldwell'] = 15
page_types['Nicole Chase'] = 16
page_types['Kathleen A. Fairchild'] = 17
page_types['David R. Couch'] = 18
page_types['Zachary B. Thoma and Dan Hauser'] = 19

"""
Requires:  `image` is a valid path to an image
"""
def cropper(image):
    pass


def main():
    outside_folders = ['00', '01', '02', '03']
    jpg_number = 1

    reader = csv.reader(open('page_types.csv', 'r'))
    
    # maps jpg_number to page_type
    page_mappings = {}
    for row in reader:
        k, v = row
        page_mappings[k] = v

    for outside_folder in outside_folders:
	
	for in_folder in range(100):
		
		inside_folder = str(in_folder)
		inside_folder = inside_folder.zfill(2)
		
		for im_num in range(100):
			
			im_num_path = str(jpg_number)
			image_path = im_num_path.zfill(6)
			image_path = outside_folder + '/' + inside_folder + '/' + image_path + '.jpg'

			if os.path.exists(image_path):
				print('sucess', image_path, jpg_number)
				jpg_number += 1
				# call function here
			else:
				print('error:', image_path)
				break

print('total images scanned:', jpg_number - 1)

    
    





if __name__=="__main__":
    main()