"""

Sample two sets of video clips from original test set.
Number of Original Video Clips: 700+

new sample file folder:
-sample
 |-set1
   |-0001
     |-c001
       |-0000_000029.jpg
       |-0001_018199.jpg
       |-...
   |-...
 |-set2


"""

import os
import shutil
import random

origin_path = "./origin"  # change as you wish
sample_path = "./sample"  # change as you wish

origin_list = os.listdir(origin_path)  # ['0001', '0002', '0003']
for f in origin_list:
    if f[0] == ".":
        origin_list.remove(f)
if not os.path.exists(sample_path):
    os.mkdir(sample_path)
set1_path = os.path.join(sample_path, "set1")  # "./sample/set1/"
set2_path = os.path.join(sample_path, "set2")  # "./sample/set2/"
if not os.path.exists(set1_path):
    os.mkdir(set1_path)
if not os.path.exists(set2_path):
    os.mkdir(set2_path)


def get_images(folder_list, set_name):
    """
    Get expected images.
    Copy them to target folder.
    :param folder_list: i.e. ['0003', '0002', '0001']
    :param set_name: target folder. i.e. "./sample/set1"
    :return: # of expected clips.
    """
    for folder in folder_list:  # i.e. folder = "0001"
        if not os.path.exists(os.path.join(set_name, folder)):
            os.mkdir(os.path.join(set_name, folder))
        inner_list = os.listdir(os.path.join(origin_path, folder))
        for folder_inner in inner_list:
            if folder_inner[0] != ".":
                files_path = os.path.join(origin_path, folder, folder_inner)
                if not os.path.exists(os.path.join(set_name, folder, folder_inner)):
                    os.mkdir(os.path.join(set_name, folder, folder_inner))
                for file in os.listdir(files_path):
                    if file[0] != ".":
                        shutil.copy(os.path.join(files_path, file), os.path.join(set_name, folder, folder_inner))
    return len(folder_list)


def sample(num):
    print(origin_list)
    set1_list = random.sample(origin_list, num)
    set2_list = random.sample(origin_list, num)
    get_images(set1_list, set1_path)
    get_images(set2_list, set2_path)
    print("Copy from origin to set1:%d and set2:%d. " % (len(set1_list), len(set2_list)))


sample(2)
