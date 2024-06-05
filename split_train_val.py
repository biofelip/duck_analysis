import glob
import shutil
import numpy as np
import argparse
import os
from tqdm import tqdm
"""This script searches for all the images of drones in a folder and splits them into train and validation sets
randomly, the names of the iamges are updated so they are different"""

# Start the parser
parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str, help='path to the root of the dataset')
parser.add_argument('--train_proportion', type=float, default=0.8, help='proportion of the dataset to be used for training')
parser.add_argument('--glob_search_pattern', type=str, default="*.JPG", help='glob search pattern')


# Parse the arguments
args = parser.parse_args()
root = args.root
train_prop = args.train_proportion
glob_search_pattern = args.glob_search_pattern

# Get all the images
full_glob_path=os.path.join(root, glob_search_pattern)
images = glob.glob(full_glob_path)
labels = glob.glob(full_glob_path.split('.')[0] +'*.txt')

# create new names that are a combination of the grandparent folder and the filename

def extract_grandparent(file, generations):
    folder=file
    for i in range(generations):
        folder=os.path.dirname(folder)
    return os.path.basename(folder)
   

# create a shuffle index
shuffle_index = np.random.permutation(len(images))

# Split the images
train_images = [images[i] for i in shuffle_index[:int(len(images)*train_prop)]]
train_labels = [labels[i] for i in shuffle_index[:int(len(images)*train_prop)]]
val_images = [images[i] for i in shuffle_index[int(len(images)*train_prop):]]
val_labels = [labels[i] for i in shuffle_index[int(len(images)*train_prop):]]

# new names
# New names
new_names_train_imgs=[extract_grandparent(file,2) + "-" + os.path.basename(file) for file in train_images]
new_names_val_imgs=[extract_grandparent(file,2) + "-" + os.path.basename(file) for file in val_images]
new_names_train_txt=[x.split('.')[0] + '.txt' for x in new_names_train_imgs]
new_names_val_txt=[x.split('.')[0] + '.txt' for x in new_names_val_imgs]

# Copy the images and labels with the new names
for image, new_name in tqdm(zip(train_images, new_names_train_imgs)):
    # check if the folder exists and create it if not
    if not os.path.exists(os.path.join(root, 'train')):
        os.makedirs(os.path.join(root, 'train'))
    shutil.copy(image, os.path.join(root, 'train', new_name))

for label, new_name in tqdm(zip(train_labels, new_names_train_txt)):
    if not os.path.exists(os.path.join(root, 'train')):
        os.makedirs(os.path.join(root, 'train'))
    shutil.copy(label, os.path.join(root, 'train', new_name))

for image, new_name in tqdm(zip(val_images, new_names_val_imgs)):
    if not os.path.exists(os.path.join(root, 'val')):
        os.makedirs(os.path.join(root, 'val'))
    shutil.copy(image, os.path.join(root, 'val', new_name))

for label, new_name in tqdm(zip(val_labels, new_names_val_txt)):
    if not os.path.exists(os.path.join(root, 'val')):
        os.makedirs(os.path.join(root, 'val'))
    shutil.copy(label, os.path.join(root, 'val', new_name))

# Copy the labels with the new names

# print(full_glob_path)
# print(len(images))
# print(len(labels))
# print(len(train_labels))
# print(len(val_labels))
