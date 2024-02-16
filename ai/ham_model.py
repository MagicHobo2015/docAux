# 
#       DocAux Image Classifier..
# 


# a ton of outside librarys used here.
import os # for path
import time # gotta know how long this takes.
import threading # specifically for the progress bar.
import numpy as np  # for numbers
import pandas as pd # for numbers
from PIL import Image   # for resizing the images
from glob import glob   # also helps with path
import seaborn as sns   # This gives us graphics.
import matplotlib.pyplot as plt # MATH
from sklearn.metrics import confusion_matrix    # this helps check accuracy.

# more some.
import keras
from keras import utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn.preprocessing import LabelEncoder
# for the spinner, it makes you feel ALIVE!
from alive_progress import alive_bar


# This is a class for my messages, there is a lot going on so I decided to split things up.
class Messages:
    def __init__(self):
        self.graphic = [
                        [' ######                   #                  '],
                        [' #     #  ####   ####    # #   #    # #    # '],
                        [' #     # #    # #    #  #   #  #    #  #  #  '],
                        [' #     # #    # #      #     # #    #   ##   '],
                        [' #     # #    # #      ####### #    #   ##   '],
                        [' #     # #    # #    # #     # #    #  #  #  '],
                        [' ######   ####   ####  #     #  ####  #    # ']
                        ]
        self.banner = "Welcome to the docAux Image Processor / Model Trainer."
        self.warning = "This takes at least 32gb of ram, and a discreete graphics card or your gonna have a bad time :)"
    
    # just to print a graphic.
    def display_graphic(self):
            for line in self.graphic:
                 print(line)

    def welcome_message(self):
         self.display_graphic()
         # give a space after that.
         print('\n\n')
         print(self.banner)
         print(self.warning)


class Configuration:
     def __init__(self) -> None:
        # This turns my print statements on or off, they are helpfull in seeing where
        # it falied.
        self.DEBUG = True
        # Scaled size for pictures. little more accurate at 64.
        self.SIZE = (64,64)
        # Seed helps with randomness.
        self.SEED = 42
        # set the spinner type from alive_progress.
        self.SPINNER = 'pulse' # 'twirls'
          


# ------------------- IMAGE PROCESSING HERE ------------------------------------
# path created and added to dataframe, now use it. This could take a while.
# Note: This takes so damn long I added a spinner from Alive-Progress (remove)
def takes_forever(configuration, skin_dataFrame):
    skin_dataFrame['image'] = skin_dataFrame['path'].map(lambda x: np.asarray(Image.open(x).resize((configuration.SIZE))))

# puts the bar and the image function together.
def process_images_with_progress(configuration, skin_dataFrame):
        with alive_bar(spinner=configuration.SPINNER) as progress_bar:
            # start a thread for the image processing so i can still do stuff
            #       while it happens
            image_thread = threading.Thread(target=takes_forever(configuration, skin_dataFrame))
            
            # start the thread.
            image_thread.start()
            
            # Just spin till the other thread is finished.
            while image_thread.is_alive():
                progress_bar()
                # slows the bar down a little, so it doesnt just go full throttle and
                #       bottleneck the image stuff.
                time.sleep(0.1)
            # Now bring the thread back in when it finishes.
            image_thread.join()
    
# Where the magic happens.
def main():
    # just for orginization.
    configuration = Configuration()
    messages = Messages()
    messages.welcome_message()

    np.random.seed(configuration.SEED)
    # Load the images into a datafram from csv file
    skin_dataFrame = pd.read_csv('./HAM10000/HAM10000_metadata.csv')

    # labels from initials to numbers
    label_encoder = LabelEncoder()
    label_encoder.fit(skin_dataFrame['dx'])
    LabelEncoder()

    ## _------------------------------------- DEBUG ----------------------------
    if configuration.DEBUG:
        # Double check that those labels are now numbers.
        print(list(label_encoder.classes_))
    ## _------------------------------------- DEBUG -END ----------------------

    # Create the paths for the images. may need to exclude a folder or two.
    image_path = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join('HAM10000/', '*', '*.jpg'))}

    # here the path is built so add it to the dataframe.
    skin_dataFrame['path'] = skin_dataFrame['image_id'].map(image_path.get)

    ## _------------------------------------- DEBUG ---------------------------
    if configuration.DEBUG:
        # lets see if that worked
        print(skin_dataFrame['dx'].value_counts())
    ## _------------------------------------- DEBUG -END ---------------------


    process_images_with_progress(configuration, skin_dataFrame)



# Need this to organize everything
if __name__ == "__main__":
    # Get the party Started.
    main()






