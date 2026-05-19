## this scripts takes random images from the image pool and puts them in a folder
## and divides them in train and val test set txt files
## then it trains a model on the train set
import os
import glob
from tkinter import Image 
import tqdm
import shutil
from  ultralytics.data.split import autosplit
from ultralytics import YOLO
root=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drohnenfotos 2025_2026"
pattern="*\\**\\*.jpg"

full_glob_path=os.path.join(root, pattern)

images = glob.glob(full_glob_path, recursive=True)
len(images)

images_to_exclude = ["DJI_20251212104104_0001_W_Wegpunkt1.JPG", 
                     "DJI_20251216113207_0001_W.JPG", 
                     "DJI_20251216113242_0002_W.JPG"]

images = [x for x in images if os.path.basename(x) not in images_to_exclude]
len(images)

## take a random subset of 300 pictures

import random

random.shuffle(images)
n_images = len(images)
n_sel = 300
selected_images = images[:n_sel]
len(selected_images)
import uuid

for image in tqdm.tqdm(selected_images):
    ext = os.path.splitext(image)[1]
    new_name = f"{uuid.uuid4().hex}{ext}"
    shutil.copy(image, os.path.join(root, "train_set2026\\images", new_name))



# use autosplit to create train and val txt files
autosplit(os.path.join(root, "train_set2026\\images"), 
          weights=(0.8, 0.2,0.0),
          annotated_only=True)


# Transform into coco format so we can use sahi slicing and train  with yolo
import globox as gx
yolo_ann = gx.AnnotationSet.from_yolo(
    folder=os.path.join(root, "train_set2026"),
    image_folder=os.path.join(root, "train_set2026", "images"),
)

# create a data.yaml file for the training
data_yaml_content = f"""
# data.yaml

# Path to the root directory of your dataset    
path: {os.path.join(root, "train_set2026")}             

# Paths to the image folders (relative to 'path')
# For autosplit, you only need to specify the main 'images' directory.
train: autosplit_train.txt
val: autosplit_val.txt

# Number of classes 
nc: 3 

# List of class names         
names: ['other', 'male', 'female'] 
"""

with open(os.path.join(root, "train_set2026", "data_auto.yaml"), "w") as f:
    f.write(data_yaml_content)

# Train model (first time 100 epochs with defaut size wqith yolo26m0)
model = YOLO('yolo26s.pt')
model = YOLO(r"runs\detect\train-4\weights\best.pt")
model = YOLO(r"runs\detect\double_descent_attempt\train\weights\last.pt")
import yaml
with open('small_object_augments.yaml', 'r') as f:
    augments = yaml.safe_load(f)


results = model.train(data=os.path.join(root, "train_set2026", "data_auto.yaml"),
                     epochs=10000,
                        batch=16,
                        imgsz=1200,
                        device=0,
                        patience=0,
                        lr0=0.0001,
                        lrf=0.01,
                        project = "double_descent_attempt2",
                        # classes=[1,2],
                        **augments)


# lets use model 12 and 28 to give me the list of files with animals
import tqdm
model12 = YOLO(r"runs\detect\train-12\weights\best.pt")
model28 = YOLO(r"runs\detect\train-28\weights\best.pt")
res12 = []

for image in tqdm.tqdm(images):
    try:
        r = model12.predict(image, conf=0.20, iou=0.2, agnostic_nms=True, augment=True)[0]
        if len(r.boxes) > 0:
            res12.append({
                "path": r.path,
                "boxes": r.boxes.xyxy.cpu().numpy(),
                "confs": r.boxes.conf.cpu().numpy(),
                "cls":   r.boxes.cls.cpu().numpy(),
            })
    except Exception as e:
        print(f"Skipping {image}: {e}")

print(f"Images with detections: {len(res12)}")

res28= []
for image in tqdm.tqdm(images):
    try:
        r = model28.predict(image, conf=0.20, iou=0.2, agnostic_nms=True, augment=True)[0]
        if len(r.boxes) > 0:
            res28.append({
                "path": r.path,
                "boxes": r.boxes.xyxy.cpu().numpy(),
                "confs": r.boxes.conf.cpu().numpy(),
                "cls":   r.boxes.cls.cpu().numpy(),
            })
    except Exception as e:
        print(f"Skipping {image}: {e}")

print(f"Images with detections: {len(res28)}")


paths12 = [x["path"] for x in res12]
boxes12 = [x["boxes"] for x in res12]
len(paths12); len(boxes12)


# move each to thei own folder in the root
from PIL import Image, ImageDraw
os.mkdir(os.path.join(root, "model12_detections"))
os.mkdir(os.path.join(root, "model12_detections", "boxes"))
for path, label in tqdm.tqdm(zip(paths12, boxes12)):
    ext = os.path.splitext(path)[1]
    new_name = f"{uuid.uuid4().hex}{ext}"
    # create image with boxes on top
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    for box in label:
        draw.rectangle(box, outline="red", width=2)
    im.save(os.path.join(root, "model12_detections","boxes",new_name))
    shutil.copy(path, os.path.join(root, "model12_detections", new_name))
