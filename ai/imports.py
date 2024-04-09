# ---------------------------------------------------------------------------- #
#   DocAux: Import file.
#
# ---------------------------------------------------------------------------- #
import os # for path
from sys import exit # so we can exit when we want.
import time # gotta know how long this takes.
import threading
import numpy as np  # for numbers
import pandas as pd # for numbers
from PIL import Image   # for resizing the images
from glob import glob   # also helps with path
import seaborn as sns   # This gives us graphics.
import matplotlib.pyplot as plt # MATH
from sklearn.metrics import confusion_matrix    # this helps check accuracy.
from math import floor

import keras
from keras import utils
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, MaxPooling2D, BatchNormalization
from sklearn.model_selection import train_test_split
from scipy import stats
import tensorflow as tf
from tensorflow.keras import utils
from sklearn.preprocessing import LabelEncoder
# for the spinner, it makes you feel ALIVE!
from alive_progress import alive_bar
from sklearn.setup import configuration
from sklearn.utils import resample