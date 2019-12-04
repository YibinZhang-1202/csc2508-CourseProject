import os

dataset_path = '../aic19-track2-reid/t'

# read img path
img_path = [os.path.join(dataset_path, x) for x in os.listdir(dataset_path) if x.startswith('set') and x.endswith('_image')]
img_path = [os.path.join(x, y) for x in img_path for y in os.listdir(x)]
img_path = [os.path.join(x, y) for x in img_path for y in os.listdir(x)]
img_path.sort()
print(img_path, '\n')

the_dir_1 = {}
the_dir_2 = {}
for x in img_path:
	the_id = os.path.split(x)[1]

	if "set1" in x:
		the_dir_1[the_id] = os.path.split(os.path.split(x)[0])[1]
	elif "set2" in x:
		the_dir_2[the_id] = os.path.split(os.path.split(x)[0])[1]

print(the_dir_1)
print(the_dir_2)


# modify keypoint path
# keypoint_path = [os.path.join(dataset_path, x) for x in os.listdir(dataset_path) if x.startswith('set') and x.endswith('_keypoint')]
# keypoint_path = [os.path.join(x, y) for x in keypoint_path for y in os.listdir(x)]
# keypoint_path = [os.path.join(x, y) for x in keypoint_path for y in os.listdir(x)]

# for x in keypoint_path:
# 	the_id = os.path.split(os.path.split(x)[0])[1]
# 	# os.rename(x, os.path.join(os.path.split(x)[0], the_id))
	
# 	start_length = the_dir[the_id]
# 	the_path = os.path.split(x)[0]
# 	print(the_path)
# 	# os.rename(the_path, os.path.join(os.path.split(the_path)[0], start_length))

# keypoint_path.sort()
# print(keypoint_path, '\n')


# # modify metadata path
# metadata_path = [os.path.join(dataset_path, x) for x in os.listdir(dataset_path) if x.startswith('set') and x.endswith('_metadata_v2m100')]
# metadata_path = [os.path.join(x, y) for x in metadata_path for y in os.listdir(x)]
# metadata_path = [os.path.join(x, y) for x in metadata_path for y in os.listdir(x)]

# for x in metadata_path:
# 	the_id = os.path.split(os.path.split(x)[0])[1]
# 	os.rename(x, os.path.join(os.path.split(x)[0], the_id))

# 	start_length = the_dir[the_id]
# 	the_path = os.path.split(x)[0]
# 	print(the_path)
# 	os.rename(the_path, os.path.join(os.path.split(the_path)[0], start_length))


# metadata_path.sort()
# print(metadata_path, '\n')