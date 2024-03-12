from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import glob
import os
import matplotlib.pyplot as plt
import folium

root=dir=root_path="E:\\drone footage\\16-11-23\\drone"
images=glob.glob(os.path.join(root_path, "**.jpg"))


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
        return((lon,lat))
    except Exception as e:
        print(f"Error: {e}")



def plot_images_pos(images):
    exif_data=[]
    for image in images:
        with Image.open(image) as img:
            exif_data.append(extract_gps_info(image))

    # we only need the second because the minutes and degrees are the same
    coords=[(x[2], y[2]) for x,y in exif_data]  
    named_coords={os.path.basenamnamee(image).split(".")[0]:coord for  image, coord in   zip(images, coords)}

    coordinates = list(named_coords.values())
    labels = list(named_coords.keys())

    # Plotting the points
    plt.scatter(*zip(*coordinates), marker='o', color='red')

    # Adding labels to each point
    for label, (x, y) in zip(labels, coordinates):
        plt.text(x, y, label)

    # Adding labels and title
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Points Plot')

    # Display the plot
    plt.show()




### here i just trry shit

exif_data=im1._getexif()

for key, val in exif_data.items():
       #if key in TAGS:
       #    print(f'{TAGS[key]}:{val}')
       #else:
        print(f'{key}:{val}')

exif_data.get(40092)
exif_data.get("0x8827")


from PIL import Image
import tqdm
import piexif

exif_dict = piexif.load(images[0])


exif_dict["0th"][271]

for ifd in ("0th", "Exif", "GPS", "1st"):
    print(ifd)
    for tag in exif_dict[ifd]:
        print(tag)
        #print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])


for ifd in ("0th", "Exif", "GPS", "1st"):
    for tag in tqdm.tqdm(exif_dict[ifd]):
         print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

exif_dict["GPS"]['GPSImgDirection']

piexif.TAGS["GPS"]