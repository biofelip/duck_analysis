"""Script to separate images into tiles it goes trhough the drone iamges and saves them into a folder called tiled_images"""

from utils import TiledImage
import glob
import os
import shutil
from tqdm import tqdm


drone_images=glob.glob("E:\\drone footage\\**\\drone\\*.jpg")