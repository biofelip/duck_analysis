from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
import os
from utils import plot_images_pos
from rasterio.plot import show
from rasterio.merge import merge
import rasterio as rio

root_path="E:\\drone footage\\08-12-23\\drone"
images=glob.glob(os.path.join(root_path, "**.jpg"))


plot_images_pos(images)

#define the pictures groups adn separe images into lines folders

group1=images[0:11]
group2=images[17:7:-1]
group3=images[18:28]
group4=images[37:27:-1]


# go to qgis and create the line rasters


line=os.path.join(root_path, "line1")
line_images=glob.glob(os.path.join(line, "**georeferenced.png"))


raster_to_mosaic=[]
for p in line_images:
    raster=rio.open(p)
    raster_to_mosaic.append(raster)

mosaic, output=merge(raster_to_mosaic)

output_meta = raster.meta.copy()
output_meta.update(
    {"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    })


with rio.open("20-11-23_line1.tif", "w",  **output_meta) as m:
    m.write(mosaic)




# variables to include
hor_overlap=0.4
ver_overlap=0.4
resize_factor=0.2



def total_picture_size( height,  vertical_overlap, num_images):
    
    #total_width = width - (horizontal_overlap * width) * (num_images - 1)
    total_height = num_images* height - (vertical_overlap * num_images* height)
    
    return  int(total_height)

def starting_positions( vertical_overlap, total_height, i): 
    starting_positions =  int((i * total_height - vertical_overlap*i*total_height))
    return starting_positions
def create_v_mosaic(group):
    resized_images=[]
    for image_name in group:
        im=Image.open(image_name)
        im_r=im.resize([int(resize_factor *s) for s in im.size])
        resized_images.append(im_r)
    height_mosaic = total_picture_size(resized_images[0].height, ver_overlap, len(resized_images))
    im_combined=Image.new('RGB', (im_r.width, height_mosaic))
    im_combined.show()
    for image in resized_images:
        start_pos=starting_positions( ver_overlap, resized_images[0].height, resized_images.index(image))
        im_combined.paste(image, (0,start_pos))

    im_combined.show()

















create_v_mosaic(group1)
create_v_mosaic(group2)
create_v_mosaic(group3)
create_v_mosaic(group4)
create_v_mosaic(group5)


