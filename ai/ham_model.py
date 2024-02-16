import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from glob import glob
from PIL import Image

# Load the images into a datafram from csv file
skin_dataFrame = pd.read_csv('HAM10000/HAM1000_metadata.csv')

# add the images to the dataframe, by reading the csv and getting the jpg from
# the csv id.
image_path = {os.path.splitext(os.path.basename(x))[0]: x for s in glob(os.path.join('HAM1000/', '*', '*.jpg'))}