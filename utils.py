from PIL.ExifTags import TAGS, GPSTAGS
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage
from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import numpy as np
import pandas as pd


def getImage(path, zoom=0.01, rescale=0.1):
    image=Image.open(path)
    image=image.resize((int(image.width*rescale), int(image.height*rescale)))
    image_ar=np.asarray(image)
    return OffsetImage(image, zoom=zoom)
def extract_gps_info(image_path):
    gps_info={}
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for key in value.keys():
                        sub_tag_name = GPSTAGS.get(key, key)
                        gps_info.update({sub_tag_name: value[key]})
        lon=gps_info.get('GPSLongitude')
        lat=gps_info.get('GPSLatitude')
        return (lon,lat)
    except Exception as e:
        print(f"Error: {e}")

def rotate_point(x, y, angle_rad):
        x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
        y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
        return x_rot, y_rot

def calculate_angle(x, y):

    # Step 1: Find the equation of the diagonal line
    coefficients = np.polyfit(x, y, 1)
    slope = coefficients[0]

    # Step 2: Calculate the angle of rotation
    angle_rad = np.arctan(slope)
    return angle_rad







# create new names that are a combination of the grandparent folder and the filename
def extract_grandparent(file, generations):
    folder=file
    for i in range(generations):
        folder=os.path.dirname(folder)
    return os.path.basename(folder)


labels_dict={"0":"Male", "1":"Female", "2":"Other"}


"""Class definition for a class of image that runs inferences and saves the results"""
class duck_image:

    def __init__(self, image_path):
        self.image_path=image_path
        self.labelfile=os.path.splitext(self.image_path)[0]+'.txt'
        self.number_of_detections={"Males":0, "Females":0, "Others":0}
        self.annotated_image=os.path.join(os.path.dirname(self.image_path), 'annotated_image', os.path.basename(self.image_path))
        self.boxes={}

    def load_image(self):
        self.image=Image.open(self.image_path)
        self.width, self.heigth =self.image.size

    def bbox(self):
        try:
            if not os.path.exists(self.labelfile):
                return
            with open(self.labelfile, 'r') as f:
                lines=f.readlines()
            if len(lines) > 0:
                lines=[x.strip('\n') for x in lines]
                for i, l in enumerate(lines):
                    cls, x, y, w, h =l.split()
                    x, y, w, h =float(x), float(y), float(w), float(h)
                    self.boxes[str(i)]={"class":cls, "xcenter":x*self.width,"x":x, "y":y, "ycenter":y*self.heigth, "width":w*self.width, "height":h*self.heigth}
        except Exception as e:
            print(f"Error: {e}")
        
    def plot(self):
        if not os.path.exists(os.path.join(os.path.dirname(self.image_path), 'annotated_image')):
                os.makedirs(os.path.join(os.path.dirname(self.image_path), 'annotated_image'))
        draw=ImageDraw.Draw(self.image)
        for i in self.boxes.keys():
                    print(i)
                    top_left = (int(self.boxes[i]["xcenter"]-self.boxes[i]["width"]/2), int(self.boxes[i]["ycenter"]-self.boxes[i]["height"]/2))
                    bottom_right = (int(self.boxes[i]["xcenter"]+self.boxes[i]["width"]/2), int(self.boxes[i]["ycenter"]+self.boxes[i]["height"]/2))
                    label = labels_dict[self.boxes[i]["class"]]
                    label_pos=(top_left[0], top_left[1]-150)
                    draw.rectangle([top_left, bottom_right], outline="red", width=15)
                    font=ImageFont.load_default(size=150)
                    draw.text(label_pos, label, fill="white", font=font, stroke_width=12, stroke_fill="red")
        self.image.save(os.path.join(os.path.dirname(self.image_path), 'annotated_image', os.path.basename(self.image_path)))
        
    def count_detections(self):
        for i in self.boxes.keys():
            if self.boxes[i]["class"] == "0":
                self.number_of_detections["Males"]+=1
            if self.boxes[i]["class"] == "1":
                self.number_of_detections["Females"]+=1
            if self.boxes[i]["class"] == "2":
                self.number_of_detections["Others"]+=1






def plot_images_pos(images, savecsv=True, plot=True):
    exif_data=[]
    counts={}
    colors=[]
    for image in images:
        exif_data.append(extract_gps_info(image))
        ducks=duck_image(image)
        ducks.load_image()
        ducks.bbox()
        ducks.count_detections()
        counts[os.path.basename(image)]=ducks.number_of_detections
        if sum(ducks.number_of_detections.values()) == 0:
            colors.append("red")
        else:
            colors.append("green")


        

    # we only need the second because the minutes and degrees are the same
    coords=[(x[2], y[2]) for x,y in exif_data]  
    named_coords={f'{os.path.basename(image).split(".")[0]}(M:{count["Males"]},F:{count["Females"]},O:{count["Others"]})':coord for  image,count,coord in   zip(images,  counts.values(), coords)}

    coordinates = list(named_coords.values())
    coordinates = [rotate_point(x, y, 0.9) for x, y in coordinates]
    print(coordinates)
    labels = list(named_coords.keys())

    # Plotting the points
    plt.scatter(*zip(*coordinates), marker='o', color=colors)

    # Adding labels to each point
    for label, (x, y) in zip(labels, coordinates):
        plt.text(x, y, label)

    # Adding labels and title
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title(str(extract_grandparent(images[0],2)))

    # CREATE A PANDAS DATAFRAME WITH ALL THE INFORMATION
    df=pd.DataFrame({"date":[extract_grandparent(image, 2) for image in images],
                    'label':labels, 
                     'latitude': [x[0] for x in coordinates], 
                     'longitude': [x[1] for x in coordinates],
                     'Males': [count["Males"] for count in counts.values()],
                     'Females': [count["Females"] for count in counts.values()],
                     'Others': [count["Others"] for count in counts.values()]})

    if savecsv:
         df.to_csv(str(os.path.dirname(images[0]))+'.csv', index=False)


    # Display the plot
    if plot:
        plt.show()