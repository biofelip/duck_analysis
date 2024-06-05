from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2 as cv
import glob
import os
model = YOLO(r"C:\Users\247404\runs\detect\train6\weights\best.pt")
image=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage\08-02-24\drone\DJI_0016.JPG"
results=model.predict(image, conf=0.20, visualize=False, augment=True)

im=results[0].plot()
imagen=cv.imread(im)
plt.imshow(im)
plt.show()

len(results[0].boxes)


# erase all annotations folders
root=r"C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage"

ann_folders=glob.glob(os.path.join(root, "**\\drone\\annotated_results"))