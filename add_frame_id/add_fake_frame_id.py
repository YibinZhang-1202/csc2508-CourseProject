import os
import sys
from random import randint

dataset_path = '../aic19-track2-reid/t'

tracklet_path = [os.path.join(dataset_path, x) for x in os.listdir(dataset_path) if x.startswith('set') and x.endswith('_image')]
tracklet_path = [os.path.join(x, y) for x in tracklet_path for y in os.listdir(x)]
tracklet_path.sort()

for x in tracklet_path:
	start_frame = randint(0, 50)
	dirlist = [i for i in os.listdir(x)]
	length = len(os.listdir(os.path.join(x, dirlist[0])))
	os.rename(os.path.join(x, dirlist[0]), os.path.join(x, str(start_frame)+'_'+str(length)) )

print(tracklet_path)