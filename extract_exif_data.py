from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import glob
import os
import folium

root=dir=root_path="E:\\drone footage\\16-11-23\\drone\\DCIM\\100MEDIA"
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





exif_data=[]
for image in images:
    with Image.open(image) as img:
        exif_data.append(extract_gps_info(image))


[print(f'{x}: {y}\n') for x,y in exif_data[0].items()]  


extract_gps_info(images[0])