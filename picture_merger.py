from PIL import Image
import glob
import os

root_path="E:\\drone footage\\16-11-23\\drone\\DCIM\\100MEDIA"
images=glob.glob(os.path.join(root_path, "**.jpg"))

# variables to include
hor_overlap=0.4
ver_overlap=0.4


im1=Image.open(images[0])
im2=Image.open(images[1])

im_combiend=Image.new('RGB', (im1.width+im2.width, im1.height))
im_combiend.show()