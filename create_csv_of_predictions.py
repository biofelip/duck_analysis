### Read trough the already classified images and create a csv file with the predictions
### addicional information like the position of the image in the flight path and iformation
## about the position of the detetectd ducks inside the the image is also calculated


from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
import os
from utils import plot_images_pos2025, duck_image, extract_gps_info
from tqdm import tqdm
from rasterio.merge import merge
import rasterio as rio

root = r"C:\Users\247404\Documents\2024\ducks\test_2025"

all_images=glob.glob(os.path.join(root, "*\\**\\*.jpg"), recursive=True)
len(all_images)
all_images = [x for x in all_images if "annotated_results" not in x]
all_images = [x for x in all_images if "annotated_image" not in x]
all_images = [x for x in all_images if "crops" not in x]
all_images = [x for x in all_images if "Totalen" not in  x]
all_images = [x for x in all_images if "DJI" in x]
plot_images_pos2025(all_images, savecsv=True, plot=False)


# Ahoa crear un csv con la informaciond de cada foto separada en un set de filas

# extract labbelled images. 
labeled = glob.glob(os.path.join(root, "*\\**\\*.txt"), recursive=True)
labeled.pop() # erase the last observations: the labels txt

images_l = [img for img in all_images if os.path.splitext(img)[0] + '.txt' in labeled]

# For ease in the future i will create a JSOn file with the labels
# first create  the full json with all images and all relevant fields
# the json will follow the COCO formatting
import json

coco_json = {
    "info": {
        "year": 2025,
        "description": "Annotated info of the dataset for the Eider ducks in the mussel farm of Kiel",
        "contributor": "Felipe Escobar",
    },
    "images": [],
    "annotations": []
}

images = []
annotations = []
id_c = 0
id_ann = 0
for image in tqdm(all_images):
    
    dict_image = {}
    dict_image["file_name"] = image
    dict_image["height"] = 4032
    dict_image["width"] = 3024
    dict_image["lat"] = {"degrees":float(extract_gps_info(image)[0][0]),
                         "minutes":float(extract_gps_info(image)[0][1]),
                         "seconds":float(extract_gps_info(image)[0][2])}
    dict_image["lon"] = {"degrees":float(extract_gps_info(image)[1][0]),
                         "minutes":float(extract_gps_info(image)[1][1]),
                         "seconds":float(extract_gps_info(image)[1][2])}
    dict_image["id"] = id_c
    ## annotatiosn dictionary
    if os.path.splitext(image)[0] + '.txt' in labeled:
        
        with open(os.path.splitext(image)[0] + '.txt', 'r') as f:
            lines = f.readlines()
        n_lines = len(lines)
        for i, l in enumerate(lines):
            dict_ann = {}
            cls, x, y, w, h =l.split()
            cls, x, y, w, h =int(cls), float(x), float(y), float(w), float(h)
            dict_ann["id"] = id_ann
            dict_ann["image_id"] = id_c
            dict_ann["category_id"] = cls
            dict_ann["bbox"] = {"center_x":x, "center_y":y, "width":w, "height":h}
            annotations.append(dict_ann)
            id_ann += 1

    images.append(dict_image)
    id_c += 1


coco_json["images"] = images
coco_json["annotations"] = annotations

# write the annotations as json file
with open("annotations_2025_test.json", "w") as f:
    json.dump(coco_json, f)


# transform the json into a csv
# read the json
with open("annotations_2025_test.json", "r") as f:
    coco_json = json.load(f)
import pandas as pd
df = pd.DataFrame(coco_json["images"])
df['lon_degrees'] = df['lon'].apply(lambda x: x['degrees'])
df['lon_minutes'] = df['lon'].apply(lambda x: x['minutes'])
df['lon_seconds'] = df['lon'].apply(lambda x: x['seconds'])
df['lat_degrees'] = df['lat'].apply(lambda x: x['degrees'])
df['lat_minutes'] = df['lat'].apply(lambda x: x['minutes'])
df['lat_seconds'] = df['lat'].apply(lambda x: x['seconds'])
df_annotations = pd.DataFrame(coco_json["annotations"])
df_annotations['center_x'] = df_annotations['bbox'].apply(lambda x: x['center_x'])
df_annotations['center_y'] = df_annotations['bbox'].apply(lambda x: x['center_y'])
df_annotations['width'] = df_annotations['bbox'].apply(lambda x: x['width'])
df_annotations['height'] = df_annotations['bbox'].apply(lambda x: x['height'])

# merge the csvs togehter with a left join 
full_df =pd.merge(df, df_annotations, how="left", left_on="id", right_on="image_id")
full_df.to_csv("annotations_2025_test.csv", index=False)


