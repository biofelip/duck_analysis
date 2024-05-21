from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2 as cv
from  ultralytics import YOLO
import numpy as np



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



"""Class definition for a class of image that allows to store tiles and inference resuls from the model"""
class TiledImage(object):
    def __init__(self, image_path, nrows, ncols ):
        self.image_path = os.path.join(image_path)
        #self.tile_size = tile_size
        self.n_rows = nrows
        self.n_cols = ncols
        self.original = cv.imread(image_path)
        self.smallest_dim=min(self.original.shape[0:2])
        self.resized_image=cv.resize(self.original, (self.smallest_dim, self.smallest_dim))
        self.tiles = []
        self.tiles_paths=[f'{os.path.splitext(os.path.basename(self.image_path))[0]}_{x}_{y}.JPG' for x in range(self.n_cols) for y in range(self.n_rows)]
        self.inferenc_results=[]
        self.number_of_detected_seals=0
        self.row_width = int(self.resized_image.shape[1] / self.n_cols)
        self.row_height = int(self.resized_image.shape[0] / self.n_rows)

    def tile_image(self):
        
        for i in range(0, self.n_cols):
            for j in range(0, self.n_rows):
                tile =self.resized_image[i * self.row_height:i * self.row_height + self.row_height, j * self.row_width:j * self.row_width + self.row_width]
                self.tiles.append(tile)

    def save_tiles(self, folder="tiles", verbose=True):
        # Check if the folder "tiles" exists if not create it
        if not os.path.exists(os.path.join(os.path.dirname(self.image_path),folder)):
            os.makedirs(os.path.join(os.path.dirname(self.image_path),folder))
        for tile, path in zip(self.tiles, self.tiles_paths):
            cv.imwrite(os.path.join(os.path.dirname(self.image_path),folder,path), tile)
            if verbose:
                print(f"Saved tile to {os.path.join(os.path.dirname(self.image_path),folder,path)}")


    def visualize_tiles(self, with_predictions=False):
        """Plot al tiles together in a n_col x n_rows matpltolib multiple label table"""
        fig, axs=plt.subplots(nrows=self.n_rows, ncols=self.n_cols)
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                axs[i,j].imshow(self.tiles[i*self.n_cols+j])
        plt.show()

    def visualize_original_square(self):
        fig, axs=plt.subplots(nrows=1, ncols=2)
        axs[0].imshow(self.original)
        axs[0].set_title("Original")
        axs[1].imshow(self.resized_image)
        axs[1].set_title("Resized")
        plt.show()

    def run_inference_on_tiles(self, model_path):
        model=YOLO(model_path)
        if len(self.tiles)==0:
            raise ValueError("No tiles to run inference on")
        self.inferenc_results= model.predict(self.tiles, imgsz=(self.row_height, self.row_width))
        self.number_of_detected_seals=sum([x.__len__() for x in self.inferenc_results])



