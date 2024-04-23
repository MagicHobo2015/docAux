import os
import time
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
import datetime
from alive_progress import alive_bar
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.utils import resample
from concurrent.futures import ThreadPoolExecutor
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Flatten,Dense,Dropout,BatchNormalization,Conv2D,MaxPooling2D
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy, categorical_crossentropy
from tensorflow.keras.metrics import Recall
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import L1L2

class Configuration:
    def __init__(self) -> None:
        self.rotation_range = 20 # rotate the images up to 20 degrees.
        self.width_shift_range = 0.10 # shift max of 5%
        self.height_shift_range = 0.10 # max of 5%
        self.generator_rescale = None # 1/255.0
        self.shear_range = 0.10
        self.zoom_range = 0.1
        self.horizontal_flip = True
        self.vertical_flip = True
        self.fill_mode = 'nearest'
        #   File Paths    
        self.training_csv = 'HAM10000/Ham_metaData.csv'
        self.testing_csv = 'HAM10000/test_data/test_data.csv'
        self.image_folder_one = 'HAM10000/ham_images/'
        self.image_folder_two = 'HAM10000/ham_images_2/'
        self.test_image_folder = 'HAM10000/test_data/images/'
        self.log_dir = 'logs/fit/'
        #   These are set with the function call
        self.training_full_paths = None
        self.testing_full_paths = None
        self.create_path()
        # Model Checkpoint
        self.checkpoint_path = 'check_points/'

    # This Function creates the dictionaries, with 
        #   { image_name : full_file_path }
    def create_path(self):

        """ This iterates over three folders, gets the path for anything with a .jpg extenstion. then makes a dictionaries to return."""

        self.training_full_paths = glob(os.path.join(self.image_folder_one, '*.jpg'))
        self.training_full_paths += glob(os.path.join(self.image_folder_two, '*.jpg'))
        
        self.testing_full_paths = glob(os.path.join(self.test_image_folder, '*.jpg'))
        
        # image path dictionaries
        self.training_full_paths = {os.path.splitext(os.path.basename(x))[0] : x for x in self.training_full_paths}
        self.testing_full_paths = {os.path.splitext(os.path.basename(x))[0] : x for x in self.testing_full_paths}
        return None

def accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)

def create_sequential_model(size):
        
        metrics = ['categorical_accuracy', Recall(),'categorical_crossentropy', ]

        i_shape = size + ( 3, )

        model=Sequential()

        model.add(Conv2D(32 , (3,3) , input_shape=i_shape, activation='relu',padding='same' , kernel_initializer='he_normal'))
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

        model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=metrics)# accuracy is also a function.

        return model

def preprocess_data(df: pd.DataFrame, size=(28,28), n_threads=4, bar_type='bubbles'):
        total_images = len(df)
        chunk_size = int(total_images / n_threads)
        split_dfs = np.array_split(df, n_threads)

        def preprocess_chunk(chunk, bar):
            # This will hold, one thread worth of image, dx
            images = []

            for path, dx in zip(chunk['path'], chunk['dx']):
                img = Image.open(path).convert('RGB').resize(size=size)
                img = np.asarray(img, dtype='float') / 255.
                images.append([img, dx])
                bar()
                # one of many threads.
            return images

        # Init the progress bar.
        with alive_bar(total=total_images, bar=bar_type) as bar:

            # This will split into threads to do the divided work.
            futures = []
            with ThreadPoolExecutor(max_workers=n_threads) as executor:
                for chunk in split_dfs:
                    future = executor.submit(preprocess_chunk, chunk, bar)
                    futures.append(future)
            split_dfs = []
            for future in futures:
                 split_dfs.append(future.result())

            # one for the img, one for the dx_label.
            x_, y_ = [], []
            for chunk_ in split_dfs:
                 for img, dx in chunk_:
                      x_.append(img)
                      y_.append(dx)
        return np.asarray(x_), np.asarray(y_)


# This is going to balance the data, needs to happen before images are inserted.
def resample_all_types_data(df: pd.DataFrame, n_samples: int) -> pd.DataFrame:
     # get the right number of 
     # just to hold the dfs for a sec.
     balanced_dfs = []

     class_types = df['dx'].unique()

     for type_ in class_types:
          # get all of each type
          dx_ = df[df['dx'] == type_]
          # resample it to the right amount
          dx_ = resample(dx_, replace=True, n_samples=n_samples, random_state=42)
          balanced_dfs.append(dx_)
     return pd.concat(balanced_dfs)


# def plot_confusion_matrix(cm, class_names):
#     figure = plt.figure(figsize=(8, 8))
#     plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
#     plt.title("Confusion matrix")
#     plt.colorbar()
#     tick_marks = np.arange(len(class_names))
#     plt.xticks(tick_marks, class_names, rotation=45)
#     plt.yticks(tick_marks, class_names)
    
#     # Normalize the confusion matrix.
#     cm = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)
    
#     # Use white text if squares are dark; otherwise black.
#     threshold = cm.max() / 2.
    
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         color = "white" if cm[i, j] > threshold else "black"
#         plt.text(j, i, cm[i, j], horizontalalignment="center", color=color)
        
#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')
#     return figure

def main():
    image_size = ( 98, 98 )
    n_samples = 500
    number_of_epochs = 150
    relevant_columns = ['dx']
    # label_fixer = LabelEncoder()
    label_fixer = OneHotEncoder(sparse_output=False)
    testing_label_fixer = OneHotEncoder(sparse_output=False)
    config = Configuration()

    # # load the csv files
    # # Columns: dx, age, sex, localization, image_id
    # training_data_frame = pd.read_csv(config.training_csv)
    # testing_data_frame = pd.read_csv(config.testing_csv)

    # #   Create The Path Columns.
    # training_data_frame['path'] = training_data_frame['image_id'].\
    #     map(config.training_full_paths.get)
    # testing_data_frame['path'] = testing_data_frame['image_id'].\
    #     map(config.testing_full_paths.get)

    # #   Clean Up the Columns.
    # training_data_frame.dropna(axis=0, how='any', subset='path', inplace=True)
    # testing_data_frame.dropna(axis=0, how='any', subset='path', inplace=True)

    # #   Resampled a Bit.
    # balanced_training_data = resample_all_types_data(training_data_frame,n_samples)

    # # data = balanced_training_data['dx'].unique().tolist()

    # train_x, train_y = preprocess_data(balanced_training_data, size=image_size, n_threads=8)
    # test_x, test_y = preprocess_data(testing_data_frame, size=image_size, n_threads=2)

    # # Last step for data processing. OneHotEncode the labels.
    # train_one_hot = label_fixer.fit_transform( train_y.reshape( -1, 1 ) )
    # test_y = testing_label_fixer.fit_transform( test_y.reshape( -1, 1 ) )


    # data_generator = ImageDataGenerator(
    #                 rotation_range=config.rotation_range,
    #                 width_shift_range=config.width_shift_range,
    #                 height_shift_range=config.height_shift_range,
    #                 rescale=config.generator_rescale,
    #                 shear_range=config.shear_range,
    #                 zoom_range=config.zoom_range,
    #                 horizontal_flip=config.horizontal_flip,
    #                 vertical_flip=config.vertical_flip,
    #                 fill_mode=config.fill_mode)

    # data_generator.fit(train_x)

    model = create_sequential_model(size=image_size)

    model.summary()

    pos_fix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = TensorBoard(log_dir=config.log_dir+pos_fix, histogram_freq=1 )

    stop_early = EarlyStopping(monitor='categorical_accuracy',patience=4,mode='auto')

    reduce_lr = ReduceLROnPlateau(monitor='categorical_accuracy', factor=0.5, patience=2, verbose=0,cooldown=0, mode='auto',min_delta=0.0001, min_lr=0)

    check_points = ModelCheckpoint(config.checkpoint_path + pos_fix, verbose=0, save_freq='epoch')

    callbacks = [check_points, stop_early, reduce_lr, tensorboard_callback]
    # callbacks = [check_points, tensorboard_callback]


    history = model.fit(data_generator.flow(train_x, train_one_hot.reshape( n_samples * 7, -1)), validation_data=(test_x, test_y.reshape(len(test_x), -1)), shuffle=True, epochs=number_of_epochs, verbose=1, callbacks=callbacks)

    model.save('models/')

if __name__ == '__main__':
    main()
