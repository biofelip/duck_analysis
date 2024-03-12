from PIL import Image
import glob
import os
from datetime import  datetime
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm

root_dir="E:\\drone footage"
directories=os.listdir(root_dir)
format_string = "%Y:%m:%d %H:%M:%S"

for directory in tqdm(directories, desc=f"Going trough directories"):
    images=glob.glob(os.path.join(root_dir, directory, "drone\*.jpg"))
    if len(images) == 0:
        continue
    else:
        times={}
        for image in tqdm(images, desc="Extracting times"):
            im=Image.open(image)
            exif=im.getexif()
            times.update({image:datetime.strptime(exif.get(306), format_string)})


    # calculate distance matrix
    dist_mat=np.zeros((len(times), len(times)))
    for i, date1 in enumerate(list(times.values())):
        for j, date2 in enumerate(list(times.values())):
            dist_mat[i, j] = abs((date1 - date2).total_seconds())
    squared_form=squareform(dist_mat)
    link_mat=linkage(squared_form, 'single')
    treshold=600
    clusters=fcluster(link_mat, treshold, 'distance')
    n_cluster=len(set(clusters))

    if n_cluster == 1:
        continue
    else:
        # create n_cluster directories if they dont exist
        for i in range(n_cluster):
            new_dir=os.path.join(root_dir, directory, 'cluster_'+str(i+1))
            # copy images to new directory only if they belong to that cluster
            images_to_copy=[image for image in images if clusters[images.index(image)] == i+1]
            if not  os.path.exists(new_dir):
                os.makedirs(new_dir)
            for image in tqdm(images_to_copy, desc="Copying images to cluster folders"):
                shutil.copy(image, os.path.join(new_dir, os.path.basename(image)))


            
            


    


