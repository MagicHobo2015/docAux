# ---------------------------------------------------------------------------- #
#   DocAux - Model evaluator                                                   #
#                                                                              #
#   Description: This module uses isic2018 test set from the HAM100000 to eval #
#       our model.                                                             #
# ---------------------------------------------------------------------------- #


from cgi import test
from operator import ne
import os
import pandas as pd
from glob import glob
from PIL import Image
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from keras.utils.np_utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class Configuration:
    def __init__(self) -> None:
        self.rotation_range = 20 # rotate the images up to 20 degrees.
        self.width_shift_range = 0.10 # shift max of 5%
        self.height_shift_range = 0.10 # max of 5%
        # self.generator_rescale = 1/255.0 # 1/255.0
        self.shear_range = 0.10
        self.zoom_range = 0.1
        self.horizontal_flip = True
        self.vertical_flip = True
        self.fill_mode = 'nearest'


def main():
    # change csv to dataframe, change labels to digits, bring in images and size them.

    model = tf.keras.models.load_model('models')
    # model.save('models')

    # Load the metadata into a DataFrame
    test_folder_path = 'HAM10000/'
    test_image_path = test_folder_path + 'test_data/images/'
    csv_file = test_folder_path + 'test_data/test_data.csv'
    dataFrame = pd.read_csv(csv_file)
    model_image_size = [64, 64]
    config_ = Configuration()

    # Now we need to get all the file names in the folder, 
    # Then use the csv names to match a full path to names.

    # Create the pattern. Use join so we can use wild cards.
    # glob uses the pattern to grab the paths.
    full_paths = glob(os.path.join(test_image_path, '*.jpg'))
    # now create a dictionary with the just the image_id as the key.
    image_paths = {os.path.splitext(os.path.basename(x))[0] : x for x in full_paths}
    # map the image paths to image ids in a new column 
    dataFrame['path'] = dataFrame['image_id'].map(image_paths.get)
    # just clean that, some how one null made it.
    dataFrame.dropna(subset=['path'], axis=0, inplace=True, how='any')

    # Now to get all the images and resize them, change rgb values.
    dataFrame['image'] = dataFrame['path'].map(lambda x: np.asarray(Image.open(x).resize(model_image_size)))

    # fix the images from 0-255 to 0-1
    test_images_x = np.asarray(dataFrame['image'].tolist()).reshape(-1,model_image_size[0], model_image_size[1],3)
    test_images_x = test_images_x / 255

    # One Hot the labels.
    one_hot = OneHotEncoder(sparse_output=False)
    data = pd.array(dataFrame['dx']).reshape(-1,1)
    test_y = one_hot.fit_transform(data)
    # print(test_images_x)

    one_hot_key = {'bkl': [0., 0., 1., 0., 0., 0., 0.], 'nv': [0., 0., 0., 0., 0., 1., 0.], 'df': [0., 0., 0., 1., 0., 0., 0.], 'mel': [0., 0., 0., 0., 1., 0., 0.], 'vasc': [0., 0., 0., 0., 0., 0., 1.], 'bcc': [0., 1., 0., 0., 0., 0., 0.], 'akiec': [1., 0., 0., 0., 0., 0., 0.]}

    image_gen = ImageDataGenerator()
    image_gen.fit(test_images_x)
    testing_data_flow = image_gen.flow(test_images_x, test_y, batch_size=128, shuffle=False)

    # results = model.evaluate(test_images_x, test_labels_y, batch_size=128)
    results = model.evaluate(testing_data_flow)

if __name__ == '__main__':
    main()