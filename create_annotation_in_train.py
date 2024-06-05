"""Creates the annotated images folder for the training images so they can be used with the rest of the
pipeline"""


import glob
import os

from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tqdm import tqdm
from utils import duck_image
from utils import extract_grandparent

#root=args.root
root=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage"

# fetch images
images=glob.glob(os.path.join(root, "**//drone//*.JPG"))


for image in tqdm(images):
    ducks=duck_image(image)
    ducks.load_image()
    ducks.bbox()
    if len(ducks.boxes) > 0: 
    #     ducks.plot()
        draw=ImageDraw.Draw(ducks.image)
        for i in ducks.boxes.keys():
                    print(i)
                    top_left = (int(ducks.boxes[i]["xcenter"]-ducks.boxes[i]["width"]/2), int(ducks.boxes[i]["ycenter"]-ducks.boxes[i]["height"]/2))
                    bottom_right = (int(ducks.boxes[i]["xcenter"]+ducks.boxes[i]["width"]/2), int(ducks.boxes[i]["ycenter"]+ducks.boxes[i]["height"]/2))
                    label = ducks.boxes[i]["class"]
                    label_pos=(top_left[0], top_left[1]-50)
                    draw.rectangle([top_left, bottom_right], outline="red", width=15)
                    font=ImageFont.load_default(size=60)
                    draw.text(label_pos, label, fill="white", font=font, stroke_width=12, stroke_fill="red")
        if not os.path.exists(os.path.join(root,extract_grandparent(image,2),'drone', 'annotated_image2')):
                os.makedirs(os.path.join(root,extract_grandparent(image,2), 'drone','annotated_image2'))
        ducks.image.save(os.path.join(root,extract_grandparent(image,2),'drone','annotated_image2', os.path.basename(image)))

