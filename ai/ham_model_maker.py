# ---------------------------------------------------------------------------- #
#                                                                              #
#   DocAux: AI Creator, Faster, less ram version                               #
#                                                                              #
# ---------------------------------------------------------------------------- #

from cgi import test
import os
from matplotlib.cbook import flatten
import pandas as pd
import numpy as np
from sys import exit
from time import sleep
import tensorflow as tf
# gives graphic visuals
# these help with overFitting
# where our model functions come from.
import matplotlib.pyplot as plt # MATH
from tensorflow.keras.metrics import Recall
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.regularizers import L1L2
# helps identify false positives, and false negatives.
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Flatten,Dense,Dropout,BatchNormalization,Conv2D,MaxPooling2D
from imblearn.over_sampling import RandomOverSampler
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy


        # A little Eye candy..
class Messages:
     def __init__(self) -> None:
        self.graphic = [
                        [' ######                   #                  '],
                        [' #     #  ####   ####    # #   #    # #    # '],
                        [' #     # #    # #    #  #   #  #    #  #  #  '],
                        [' #     # #    # #      #     # #    #   ##   '],
                        [' #     # #    # #      ####### #    #   ##   '],
                        [' #     # #    # #    # #     # #    #  #  #  '],
                        [' ######   ####   ####  #     #  ####  #    # ']
                        ]
        
        self.config_message = 'Initializing Configuration...'
        self.welcome_message = 'Welcome to DocAux Ai Model maker'
        self.no_save_message = 'It Looks like you are exiting without saving your model. Would you like to continue? (y/N)?'
        self.menu_options = ['Please Make A Selection: ',
                             '1.\t Process Image Data ',
                             '2\t Create Model ',
                             '3.\t Train Model ',
                             '4.\t Save Model ',
                             '5.\t Exit DocAux AI maker']
        self.process_data_message = 'Thanks for choosing Data Processing. \n, This script uses dataGenerator to alter images that we dont have enough of. This can be configured in the configuration file.'
        self.csv_message = 'If you would like to choose a specific csv file, \n enter it here: \t'
        self.file_not_found = 'Oops! It looks like your csv File is missing.'
        self.finished_processing = '\n Data Processed, Ready to Create Model \n'

     def config_notification(self):
          print(self.config_message)      
     def welcome(self):
        for line in self.graphic:
            print(line)
        # need a space between banner and content.
        print('\n')
        print(self.welcome_message)
        sleep(.5)
          
     def display_menu(self) -> str:
          for option in self.menu_options:
            print(option)

     def no_save_warning(self):
            print(self.no_save_message)

     def process_data(self):
          print(self.process_data_message)

     def get_csv_file(self):
          possible_csv = input(self.csv_message)
          return possible_csv
     
     def use_csv(self, configuration):
         print('Using {configuration.csv_file}, if you would like to use another, this can be changed in the config file. Make sure to match the input the model expects.')
       

class Configuration:
    def __init__(self) -> None:
        self.base_dir = './HAM10000'
        self.csv_file = 'hmnist_28_28_RGB.csv'
        self.train_split = (0.75, 0.25)
        self.random_seed = 42 # the meaning of life.
        self.saved = False
        self.debug = True

        # Image generator config. ----------------------------------------------
        self.rotation_range = 20 # rotate the images up to 20 degrees.
        self.width_shift_range = 0.10 # shift max of 5%
        self.height_shift_range = 0.10 # max of 5%
        self.generator_rescale = 1./255
        self.shear_range = 0.10
        self.zoom_range = 0.1
        self.horizontal_flip = True
        self.vertical_flip = True
        self.fill_mode = 'nearest'

        # Training configuration ---------------------------------------------
        # alter these at your own risk!
        self.class_weights = {0:1,1:0.5,2:1,3:1,4:1,5:1,6:1}
        self.epochs = 20
        self.batch_size = 128
        self.stop_early = True


# can automate this but here we are.
label={
    ' Actinic keratoses':0,
    'Basal cell carcinoma':1,
    'Benign keratosis-like lesions':2,
    'Dermatofibroma':3,
    'Melanocytic nevi':4,
    'Melanoma':6,
    'Vascular lesions':5
}

def accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)

# this is a cnn model
def create_sequential_model():
        model=Sequential()

        model.add(Conv2D(32 , (3,3) , input_shape=(28,28,3), activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Conv2D(64,(3,3),input_shape=(28,28,3),activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(Conv2D(64 , (3,3) , activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Conv2D(128,(3,3),input_shape=(28,28,3),activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(Conv2D(128,(3,3),input_shape=(28,28,3),activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Conv2D(256,(3,3),input_shape=(28,28,3),activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(Conv2D(256,(3,3),input_shape=(28,28,3),activation='relu',padding='same' , kernel_initializer='he_normal'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(units=256, activation = 'relu', kernel_initializer='he_normal'))
        model.add(BatchNormalization())
        model.add(Dense(units=128, activation = 'relu', kernel_initializer='he_normal'))
        model.add(BatchNormalization())
        model.add(Dense(units=64, activation = 'relu', kernel_initializer='he_normal'))
        model.add(BatchNormalization())
        model.add(Dense(units=32, activation = 'relu', kernel_initializer='he_normal', kernel_regularizer=L1L2()))
        model.add(BatchNormalization())
        model.add(Dense(units=7, activation='softmax', kernel_initializer='glorot_uniform', name='classifier'))


        model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=[accuracy, Recall()])

        return model

# this only works after the model has been trained.
def display_accuracy_graph(model_history):
     #Visualizing Training and Validation Accuracy
     plt.figure(figsize=(15,5))
     loss=pd.DataFrame(model_history.history)
     loss=loss[['accuracy','val_accuracy']]
     loss.plot()
     input("Press enter to continue.")


# saves whatever version of the model you want, default is both.
def save_our_models(model, file_name='ham_cancer_model.h5', version='both'):
        if version == 'both':
            # save the dev version.
            model.save(file_name, overwrite=True)
            # save the production version.
            tf.saved_model.save(model, 'models')
        elif version == 'development':
             model.save(file_name)
        
        elif version == 'production':
            tf.saved_model.save(model, 'models')


def load_model(model_path):
  """Loads a TensorFlow model based on its file extension.

  Args:
      model_path: The path to the model file.

  Returns:
      The loaded TensorFlow model.

  Raises:
      ValueError: If the file extension is not supported.
  """
  _, ext = os.path.splitext(model_path)
  if ext == ".h5":
    return tf.keras.models.load_model(model_path)
  elif ext == ".pb":
    # Handle `.pb` format (usually for frozen models)
      return tf.saved_model.load(model_path)
  else:
    raise ValueError(f"Unsupported file extension: {ext}")


# where all the work is done.
def main():
    # Let us talk with the user
    messages = Messages()

    # Prints welcome messages.
    messages.welcome()
    running = True
    # initialize config variables.
    config_ = Configuration()

    while running:
        # display menu and get user input.
        selections = ['1', '2', '3', '4', '5', '6']
        selection = None
        messages.display_menu()

        while selection not in selections:
             selection = input('Selection: ')

        if selection == '1':    # Process data
            # inform where to change csv.
            messages.use_csv(config_)
            # use the prescaled csv
            try:
                skin_dataFrame = pd.read_csv(os.path.join(config_.base_dir,
                                                    config_.csv_file))
            except FileNotFoundError:
                print(messages.file_not_found)

            oversample = RandomOverSampler()

            x = skin_dataFrame.drop('label', axis=1)
            print(x)
            y = skin_dataFrame['label']

            x, y = oversample.fit_resample(x, y)
            x = np.array(x).reshape(-1,28,28,3)

            y = np.array(y)

            if config_.debug:
                print(y)
                print(f'Shape: \t \t {x.shape}')
                print(f'yShape: \t {y.shape}')

            # split the dataset
            train_set_images, test_set_images, train_set_labels, test_set_labels = train_test_split(x, y, test_size=config_.train_split[-1], random_state=config_.random_seed)

            train_set_labels = to_categorical(train_set_labels)
            test_set_labels = to_categorical(test_set_labels)

            # For better accuracy ImageGenerater.
            # dataGenerator initialized here.
            data_generator = ImageDataGenerator(
                rotation_range=config_.rotation_range,
                width_shift_range=config_.width_shift_range,
                height_shift_range=config_.height_shift_range,
                rescale=config_.generator_rescale,
                shear_range=config_.shear_range,
                zoom_range=config_.zoom_range,
                horizontal_flip=config_.horizontal_flip,
                vertical_flip=config_.vertical_flip,
                fill_mode=config_.fill_mode)
            
            # this will fluff up the images. it rotates and flips and makes new ones.
            test_generator = ImageDataGenerator(rescale=(1./255))

            data_generator.fit(train_set_images)
            test_generator.fit(test_set_images)
            print(messages.finished_processing)

        elif selection == '2':  # Create Model
            # Compiles the model.
            model_v2 = create_sequential_model()

            # Gives info about the model.
            model_v2.summary()
        elif selection == '3':  # Train Model
            # in development.
            if config_.stop_early:
                # This section helps with overfitting.
                stop_early = EarlyStopping(monitor='accuracy',patience=4,mode='auto')
                reduce_lr = ReduceLROnPlateau(monitor='accuracy', factor=0.5, patience=2, verbose=1,cooldown=0, mode='auto',min_delta=0.0001, min_lr=0)
            
            training_data = data_generator.flow(train_set_images, train_set_labels, shuffle=True)
            validation_data = test_generator.flow(test_set_images, test_set_labels, shuffle=True)
            callbacks = ([stop_early,reduce_lr] if config_.stop_early else None)

            # time to train.
            model_v2.fit(
                training_data,
                batch_size=config_.batch_size,
                epochs=config_.epochs,
                # class_weight=config_.class_weights, # i dunno.
                validation_data=validation_data,
                verbose=1,
                callbacks=callbacks)
            
            save_our_models(model_v2, 'Temp.h5')
            # see how it went.
            history = model_v2.history
            display_accuracy_graph(history)
        elif selection == '4':  # Save Model
             if not config_.saved:
                config_.saved = True
             save_our_models(model_v2)                        
        elif selection == '5':  # Exit the program
            if not config_.saved:
                cont = input(messages.no_save_message)
                if cont.upper() == 'Y': 
                    running = False
                    exit()
                elif cont == 'N' or cont == '':
                    pass
            else:
                save_our_models(model_v2)

        elif selection == '6': # load a model
            getting_input = True
            while getting_input:
                file_path = input("Enter the file path: ")
            if os.path.exists(file_path):
                model_to_load = file_path
                getting_input = False
            else:
                print("File does not exist. Please enter a valid file path.")
            
            loaded_model = load_model(model_to_load)


if __name__ == '__main__':
     main()