# ---------------------------------------------------------------------------- #
#                                                                              #
#   DocAux: AI Creator Configuration file.                                     #
#                                                                              #
# ---------------------------------------------------------------------------- #
from imports import np

class Configuration:
     # initialize all this stuff.
     def __init__(self) -> None:
        # This turns my print statements on or off, they are helpfull in seeing
        #   where it falied.
        self.DEBUG = True
        # graphs on/off
        self.visualization = True
        # Scaled size for pictures. little more accurate at 64.
        self.SIZE = (64,64)
        # Seed helps with randomness.
        self.SEED = 42
        # Number to balance images too.
        self.sample_size = 500 # default sample size.
        # set the spinner type from alive_progress.
        self.SPINNER = 'pulse' # 'twirls'
        # Path to the CSV file containing metadata
        self.ham_csv = './HAM10000/HAM10000_metadata.csv'
        self.isic_csv = 'isic_training_test_data/'
        # an 80 - 20 split for training and testing.
        self.train_test_split = np.array([0.9,0.1])
        self.batch_size = 90 # adjust for you
        self.epochs = 50
        # Change these at your own risk
        self.class_weights = {0:1,1:0.5,2:1,3:1,4:1,5:1,6:1}
