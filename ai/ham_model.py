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
from sklearn.utils import resample


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
        self.loaded_message = '\n\npicture processing complete. \n'
        self.options = '1.\t Show Graphs\n' + '2.\t Fix Samples\n' + '3.\t Exit\n'
        self.resample = 'To Fix the samples we are going to upscale some and downscale others to meet somewhere in the middle'
    
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
        # This turns my print statements on or off, they are helpfull in seeing
        #   where it falied.
        self.DEBUG = True
        # Scaled size for pictures. little more accurate at 64.
        self.SIZE = (64,64)
        # Seed helps with randomness.
        self.SEED = 42
        # Number to balance images too.
        self.sample_size = 500
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
            
            print('\nLooks Like Everything went well and all the photos are loaded into ram\n')


# This function takes care of building the graphs.
def visualize_our_data(skin_dataFrame):
    # Some graphs to help visualize the data.
    # Everything will be placed on this so play with size to make it look good.
    fig_size = (15,10)
    fig = plt.figure(figsize=fig_size)  # I know its bad to shadow but
                                        #   im running low on names
    # Start with a bar graph to show cancer types and thier image
    # counts.
    # ctc = cancer type, count.
    number_of_rows, number_of_columns, fig_index = 2, 2, 1 # Upper left
    # add graph to figure.
    ctc_graph = fig.add_subplot(number_of_rows,number_of_columns, 
                                fig_index)
    #   Give the data, the count for each type.
    skin_dataFrame['dx'].value_counts().plot(kind='bar',
                                            ax=ctc_graph)
    
    # Now a couple labels so we can tell what were looking at.
    ctc_graph.set_ylabel("Totals")
    ctc_graph.set_title('Cancer Image counts.')

    # Next up sex (giggity).
    # index two should be on the right.
    fig_index += 1
    # second graph added here.
    sex_graph = fig.add_subplot(number_of_rows,number_of_columns,fig_index)
    # get the values and count how many of each then send them to the right
    # place.
    skin_dataFrame['sex'].value_counts().plot(kind='bar', ax=sex_graph)
    # next set the labels,
    sex_graph.set_ylabel('Totals')
    sex_graph.set_label('Sex! ;)')

    # Now for location.
    fig_index += 1 
    # add the graph to the figure.
    location_graph = fig.add_subplot(number_of_rows, number_of_columns,
                                    fig_index)
    # give it some data.
    skin_dataFrame['localization'].value_counts().plot(kind='bar')
    location_graph.set_ylabel('Totals')
    location_graph.set_label('Localization')

    # Last one worth looking at.
    # gonna do something a little different for this
    fig_index +=1
    # add the graph to the canvas.
    age_graph = fig.add_subplot(number_of_rows, number_of_columns, fig_index)
    sample_ages = skin_dataFrame[pd.notnull(skin_dataFrame['age'])]
    # show a normal line too, to see distribution easily.
    sns.distplot(sample_ages['age'], fit=stats.norm, color='red')
    age_graph.set_title('Age')    
    return fig


def change_number_of_images(sample_number: int, dataFrame_to_alter: pd.DataFrame)->pd.DataFrame:
    pass


# Where the magic happens.
def main():
    # just for orginization.
    configuration = Configuration()
    messages = Messages()
    messages.welcome_message()

    np.random.seed(configuration.SEED)
    # debug runs from the base dir, but I like to run from the ai folder.
    # Run From base.
    # 
    # ham_csv = './ai/HAM10000/HAM10000_metadata.csv'
    ham_csv = './HAM10000/HAM10000_metadata.csv'
    # Load the images into a datafram from csv file
    skin_dataFrame = pd.read_csv(ham_csv)
    # labels from initials to numbers
    label_encoder = LabelEncoder()
    label_encoder.fit(skin_dataFrame['dx'])
    LabelEncoder()
    ## ------------------------------------- DEBUG ----------------------------
    if configuration.DEBUG:
        # The values before transformation.
        print(list(label_encoder.classes_))
    ## ------------------------------------- DEBUG -END ----------------------
    skin_dataFrame['label'] = label_encoder.transform(skin_dataFrame["dx"])
## ------------------------------------- DEBUG ----------------------------
    if configuration.DEBUG:
        # Double check that those labels are now numbers.
        print(list(skin_dataFrame['label'].value_counts()))
    ## ------------------------------------- DEBUG -END ----------------------
    # Create the paths for the images. may need to exclude a folder or two.
    image_path = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join('HAM10000/', '*', '*.jpg'))}
    # here the path is built so add it to the dataframe.
    skin_dataFrame['path'] = skin_dataFrame['image_id'].map(image_path.get)
    ## _------------------------------------- DEBUG ---------------------------
    if configuration.DEBUG:
        # lets see if that worked
        print(skin_dataFrame['dx'].value_counts())
    ## _------------------------------------- DEBUG -END ---------------------
    # once done, you have all the photos size corrected and loaded in ram
    #process_images_with_progress(configuration, skin_dataFrame)
    ## _------------------------------------- DEBUG ---------------------------
    if configuration.DEBUG:
        # Get a little taste, proof of life.
        print(skin_dataFrame.sample(10))
    ## _------------------------------------- DEBUG -END ---------------------
    
    # Here we have some choices to make.
    print(messages.loaded_message)
    _next = input(messages.options)
    choosing = True

    while choosing:
        if _next == "1":
            graph_of_data = visualize_our_data(skin_dataFrame)
            graph_of_data.tight_layout()
            graph_of_data.show()
            # need this to keep the plot alive.
            choosing = input('Enter False to continue')
        # Here we will balance the data.    
        elif _next == "2":
            choosing = False
            # here we will grab a balanced set of images to train.
            # start with a list of labels
            list_of_labels = skin_dataFrame['label'].unique()
    ## _------------------------------------- DEBUG ---------------------------
            if configuration.DEBUG:
                print(f'The List of Unique Labels is:\n \t\t {list_of_labels}')
    ## _------------------------------------- DEBUG -END ---------------------
            temp = []
            for index, label in enumerate(list_of_labels):
                # to balance everything, make new section to separate them all.
                data_row = skin_dataFrame[skin_dataFrame['label'] == index]
                temp.append(data_row)
        
            # loop through the separate sections 0-6
            for count, row in enumerate(temp):
                # resample it and go up or down 
                # randomly to meet at sample_size.
                temp[count] = resample(row, replace=True, n_samples=configuration.sample_size, random_state=configuration.SEED)

            balanced_skin_dataFrame = pd.concat(temp, ignore_index=True)

            print(balanced_skin_dataFrame)
### NOTE: HERE The Images are loaded, 500 of each have been selected randomly 
            graph_of_data = visualize_our_data(balanced_skin_dataFrame)
            graph_of_data.tight_layout()
            graph_of_data.show()
            input("press")




        elif _next == "3":
            choosing = False
            print(messages.resample)
            number_of_samples = input("Please enter a number of samples to normalize too.") # start with 500
            return
        else:
            _next = input(messages.loaded_message)
            

    
# Need this to organize everything
if __name__ == "__main__":
    # Get the party Started.
    main()






