from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
import os

root_path="E:\\drone footage\\16-11-23\\drone"
images=glob.glob(os.path.join(root_path, "**.jpg"))

# variables to include
hor_overlap=0.4
ver_overlap=0.4
resize_factor=0.4



im1=Image.open(images[0])
im2=Image.open(images[1])

im1_r=im1.resize([int(resize_factor *s) for s in im1.size])
im2_r=im2.resize([int(resize_factor *s) for s in im2.size])

im1_r.save("im1_r.jpg")
im2_r.save("im2_r.jpg")
# vertical merging the image has width of im1 and im2 but 0.8* height of im1+im2
im_combiend=Image.new('RGB', (im1_r.width, int(0.8*(2*im1_r.height))))
im_combiend.show()