import glob
import bubble_extractor

glob_list = glob.glob("June ICC ABS/Batch0??/Images/*")

f = open('bad_timing_marks.txt', 'w+')

bad_paths = []
count = 0
total_count = 0

for image_path in sorted(glob_list):
	# left, right, top, bottom = bubble_extractor.countContours(image_path)
	
	# if right != 47 or left != 47 or top != 32 or bottom != 33:
	# 	bad_paths.append(image_path)
	# 	f.writelines(image_path)
	# 	print(image_path)

	len_right, len_left, len_tops, len_bottoms = bubble_extractor.countContours(image_path)

	total_count += 1
	if len_right != 47 or len_tops != 32 or len_bottoms != 33 or len_left != 47:
		count += 1
		print(len_right, len_left, len_tops, len_bottoms, image_path, file=f)
		print(image_path)


	# top_left = bubble_extractor.countContours(image_path)

	# if len(top_left) != 1:
	# 	breakpoint()
	# 	count += 1
	# 	print(image_path)

# f.close()
print("\n\n",count, total_count, count/total_count, file=f)