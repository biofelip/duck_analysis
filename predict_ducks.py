from ultralytics import YOLO
import os
import glob 
import argparse
from tqdm import tqdm
from PIL import Image
import cv2 as cv
import matplotlib.pyplot as plt
"""This script run the pretrained model and saves the predicted labels of the images in a txt file so i can manually check them
in yololabeler, it also saves the cuts and the annotated images"""

# Start the parser and parse the arguments
parser = argparse.ArgumentParser()


parser.add_argument('--root', type=str, help='path to the root of the dataset')
parser.add_argument('--model', type=str, help='path to the model')
parser.add_argument('--glob_search_pattern', type=str, default="*.JPG", help='glob search pattern')
parser.add_argument('--confidence', type=float, default=0.19, help='confidence threshold')

root=parser.parse_args().root
model=parser.parse_args().model
pattern=parser.parse_args().glob_search_pattern
confidence=parser.parse_args().confidence

# # get all the images
# root=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage\08-02-24"
# model=r"C:\Users\247404\runs\detect\train6\weights\best.pt"
# pattern="drone\*.jpg"
# confidence=0.20


full_glob_path=os.path.join(root, pattern)
images = glob.glob(full_glob_path, recursive=True)

# run inference on all images

model = YOLO(model)
results=[]
for image in tqdm(images, total=len(images)):
    results = model.predict(image, conf=confidence, iou=0.50, agnostic_nms=True, augment=True)
    # if len(results.boxes) > 0:
    #     im_array = results.plot()  # plot a BGR numpy array of predictions
    #     im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    #     plt.imshow(im)
    #     plt.show()


# save resuls and crops of the detections inside the drone folder

    for i, r in tqdm(enumerate(results), total=len(results)):
        dirname_image=os.path.dirname(image)
        txt_name=os.path.join(dirname_image, os.path.splitext(image)[0]+'.txt')
        r.save_txt(os.path.join(dirname_image, txt_name))
        #save  annotades results images
        annotated_results_dir=os.path.join(dirname_image, 'annotated_results')
        if not os.path.exists(annotated_results_dir):
            os.makedirs(annotated_results_dir)
        # save annotated image
        if len(r.boxes) > 0: 
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save(os.path.join(annotated_results_dir, os.path.basename(image)))
        # save cropped ducks to check
        crops_dir=os.path.join(dirname_image, 'crops')                   
        if not os.path.exists(crops_dir):
            os.makedirs(crops_dir)
        image_folder=os.path.join(crops_dir, os.path.basename(os.path.splitext(image)[0]))
        r.save_crop(save_dir=image_folder)




