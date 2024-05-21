from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import glob
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox




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



def plot_images_pos(images):
    exif_data=[]
    for image in images:
        exif_data.append(extract_gps_info(image))

    # we only need the second because the minutes and degrees are the same
    coords=[(x[2], y[2]) for x,y in exif_data]  
    named_coords={os.path.basename(image).split(".")[0]:coord for  image, coord in   zip(images, coords)}

    coordinates = list(named_coords.values())
    coordinates = [rotate_point(x, y, 0.9) for x, y in coordinates]
    print(coordinates)
    labels = list(named_coords.keys())

    # Plotting the points
    plt.scatter(*zip(*coordinates), marker='o', color='red')

    # Adding labels to each point
    for label, (x, y) in zip(labels, coordinates):
        plt.text(x, y, label)

    # Adding labels and title
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Check which picture belong to each line')

    # Display the plot
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

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
    # Step 3: Rotate the points
