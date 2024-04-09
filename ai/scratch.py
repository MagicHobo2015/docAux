import os
import shutil
import pandas as pd
from glob import glob
from pathlib import Path



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


class Configuration():

    def __init__(self) -> None:
        self.parent = 'HAM10000/'
        self.old_folders = [ 'HAM10000/ham_images/', 'HAM10000/ham_images_2/' ]
        self.csv = None
        self._classes = None


    def create_directory(self, dir: str):
        Path(dir).mkdir(parents=True, exist_ok=True)


config = Configuration()
config.csv = pd.read_csv('HAM10000/Ham_metaData.csv')

config._classes = config.csv['dx'].unique()

grouped = config.csv.groupby('dx')
sub_frames = [group for _, group in grouped]

# Takes time, searches for all jpb in ham folder.
paths = glob(os.path.join('HAM10000/**/*.jpg'), recursive=True )
# maps image_id to a full path.
img_paths_hash = {os.path.splitext(os.path.basename(x))[0] : x for x in paths}

for df  in sub_frames:
    # make a folder
    dir = 'images/'
    destination = dir + df['dx'].unique()[0]
    current_csv = df['dx'].unique()[0] + '.csv'

    config.create_directory(destination)

    for id in df['image_id']:
        source = img_paths_hash.get(id)
        message = f'Moving File: { id }, from: { source }, to:\
        { destination }'

        print(message)
        shutil.move(source, destination)

        # Now the file should be moved, so double check
        # get a list of everything inside new folder.
        verify = os.listdir(destination)

        if id in verify:
            print('Confirmed')
        else:
            print('Failed')

    # Save the relavent portion of csv
    df.to_csv(current_csv)