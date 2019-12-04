import os
import sys
from random import randint

dataset_path = '../aic19-track2-reid/t'

tracklet_path = [os.path.join(dataset_path, x) for x in os.listdir(dataset_path) if x.startswith('set') and x.endswith('_image')]
tracklet_path = [os.path.join(x, y) for x in tracklet_path for y in os.listdir(x)]
tracklet_path.sort()
# print(tracklet_path)

for x in tracklet_path:
	start_frame = randint(0, 50)
	dirlist = [i for i in os.listdir(x)]
	length = len(os.listdir(os.path.join(x, dirlist[0])))
	new_name = str(start_frame).zfill(2) +'_'+str(length)

	the_id = os.path.split(x)[1]
	print(x)

	# print(the_id)
	os.rename(os.path.join(x, dirlist[0]), os.path.join(x, the_id))

	os.rename(x, os.path.join(os.path.split(x)[0], new_name))

