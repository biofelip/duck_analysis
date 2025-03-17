# this script creates a random partition of the counted data and then separates the 
# selected images and labels into  a new folder for me to check manuallyu

import json
import random
import tqdm
import shutil
import os

with open("annotations_2025.json", "r") as f:
    coco_json = json.load(f)

images = coco_json["images"]
random.shuffle(images)
n_images = len(images)
n_sel = int(n_images * 0.1)
selected_images = images[:n_sel]

for image in tqdm.tqdm(selected_images):
    image_id = image["id"]
    image_name = image["file_name"]
    # copy the image to new location but named it using the image id
    shutil.copy(image_name, os.path.join(r"C:\Users\247404\Documents\2024\ducks\test_2025", str(image_id)+".JPG"))
    if os.path.exists(image_name.replace(".JPG", ".txt")):
        shutil.copy(image_name.replace(".JPG", ".txt"), os.path.join(r"C:\Users\247404\Documents\2024\ducks\test_2025", str(image_id)+".txt"))


## no go and label the images at the end you should have a new json file and a new csv

# load the predictions from the csvs



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# Load CSVs
predicitons2025 = pd.read_csv("annotations_2025.csv")

predicitons_test = pd.read_csv("annotations_2025_test.csv")
predicitons_test['superid'] = predicitons_test['id_x'].astype(str) + predicitons_test['center_x'].astype(str) +predicitons_test['center_y'].astype(str)
predicitons2025['superid'] = predicitons2025['id_x'].astype(str) + predicitons2025['center_x'].astype(str) +predicitons2025['center_y'].astype(str)


# Merge the DataFrames based on the `superid` column
predictions_merged = pd.merge(predicitons_test, predicitons2025, how="outer", on="superid")
predictions_merged['category_id_x'].value_counts()
predictions_merged['category_id_y'].value_counts()

# remove label 2 from both groups
predictions_merged = predictions_merged[predictions_merged['category_id_x'] != 2]
predictions_merged = predictions_merged[predictions_merged['category_id_y'] != 2]

y_true = [1 if x else 0 for x in predictions_merged["category_id_x"]]

y_pred =[1 if x else 0 for x in predictions_merged["category_id_y"]]

# Compute confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Display confusion matrix
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=set(y_true), yticklabels=set(y_true))
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()

# Print detailed classification report
print(classification_report(y_true, y_pred))


## with pycooc dios nos salve
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import json

with open("annotations_2025_test.json", "r") as f:
    test = json.load(f)
with open("annotations_2025_only_ann.json", "w") as f:
    json.dump(test['annotations'], f)
with open("annotations_2025.json", "r") as f:
    pred = json.load(f)
cocoGt = COCO("annotations_2025_only_ann.json")  # Load GT annotations in COCO format
cocoDt = cocoGt.loadRes()    # Load predictions in COCO format

evaluator = COCOeval(cocoGt, cocoDt, "bbox")
evaluator.evaluate()
evaluator.accumulate()
evaluator.summarize()
