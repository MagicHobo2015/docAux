# 
#       DocAux Image Classifier..  This version doesnt work!!! YOU WANT ham_model_maker.y
# 
from old_stuff.imports import *
from old_stuff.myConfig import Configuration

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
        self.balanced_data = False
    
    def resample_message(self, sample_size: int):
        print(f'To Fix the samples we are going to upscale some and downscale others to meet somewhere in the middle\n adjusting everything to {sample_size}')
    
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

    def show_classes(self, label_encoder):
        print(list(label_encoder.classes_))

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


# # This function takes care of building the graphs.
# def visualize_our_data(skin_dataFrame):
#     # Some graphs to help visualize the data.
#     # Everything will be placed on this so play with size to make it look good.
#     fig_size = (15,10)
#     fig = plt.figure(figsize=fig_size)  # I know its bad to shadow but
#                                         #   im running low on names
#     # Start with a bar graph to show cancer types and thier image
#     # counts.
#     # ctc = cancer type, count.
#     number_of_rows, number_of_columns, fig_index = 2, 2, 1 # Upper left
#     # add graph to figure.
#     ctc_graph = fig.add_subplot(number_of_rows,number_of_columns, 
#                                 fig_index)
#     #   Give the data, the count for each type.
#     skin_dataFrame['dx'].value_counts().plot(kind='bar',
#                                             ax=ctc_graph)
    
#     # Now a couple labels so we can tell what were looking at.
#     ctc_graph.set_ylabel("Totals")
#     ctc_graph.set_title('Cancer Image counts.')

#     # Next up sex (giggity).
#     # index two should be on the right.
#     fig_index += 1
#     # second graph added here.
#     sex_graph = fig.add_subplot(number_of_rows,number_of_columns,fig_index)
#     # get the values and count how many of each then send them to the right
#     # place.
#     skin_dataFrame['sex'].value_counts().plot(kind='bar', ax=sex_graph)
#     # next set the labels,
#     sex_graph.set_ylabel('Totals')
#     sex_graph.set_label('Sex! ;)')

#     # Now for location.
#     fig_index += 1 
#     # add the graph to the figure.
#     location_graph = fig.add_subplot(number_of_rows, number_of_columns,
#                                     fig_index)
#     # give it some data.
#     skin_dataFrame['localization'].value_counts().plot(kind='bar')
#     location_graph.set_ylabel('Totals')
#     location_graph.set_label('Localization')

#     # Last one worth looking at.
#     # gonna do something a little different for this
#     fig_index +=1
#     # add the graph to the canvas.
#     age_graph = fig.add_subplot(number_of_rows, number_of_columns, fig_index)
#     sample_ages = skin_dataFrame[pd.notnull(skin_dataFrame['age'])]
#     # show a normal line too, to see distribution easily.
#     sns.distplot(sample_ages['age'], fit=stats.norm, color='red')
#     age_graph.set_title('Age')
#     fig.tight_layout()
#     fig.show()
#     # need this to keep the plot alive.
#     pause = True
#     while pause:
#         pause = False if input('Press 0 to continue') == "0" else True
#     return pause

def visualize_our_data(skin_dataFrame):
    """
    Visualize the skin cancer data using various graphs.

    Args:
        skin_dataFrame (pd.DataFrame): DataFrame containing skin cancer data.

    Returns:
        bool: True if the user chooses to pause the plot, False otherwise.
    """
    # Set the size of the figure
    fig_size = (15, 10)
    fig = plt.figure(figsize=fig_size)

    # Plot 1: Bar graph showing cancer types and their image counts
    ax1 = fig.add_subplot(2, 2, 1)
    skin_dataFrame['dx'].value_counts().plot(kind='bar', ax=ax1)
    ax1.set_ylabel("Totals")
    ax1.set_title('Cancer Image Counts')

    # Plot 2: Bar graph showing distribution of sex
    ax2 = fig.add_subplot(2, 2, 2)
    skin_dataFrame['sex'].value_counts().plot(kind='bar', ax=ax2)
    ax2.set_ylabel('Totals')
    ax2.set_title('Sex')

    # Plot 3: Bar graph showing distribution of lesion localization
    ax3 = fig.add_subplot(2, 2, 3)
    skin_dataFrame['localization'].value_counts().plot(kind='bar', ax=ax3)
    ax3.set_ylabel('Totals')
    ax3.set_title('Localization')

    # Plot 4: Distribution of ages with normal distribution curve
    ax4 = fig.add_subplot(2, 2, 4)
    sample_ages = skin_dataFrame[pd.notnull(skin_dataFrame['age'])]
    sns.distplot(sample_ages['age'], fit=stats.norm, color='red', ax=ax4)
    ax4.set_title('Age')

    # Adjust layout and display the plot
    fig.tight_layout()
    plt.show()

    # Ask user to pause or continue
    pause = True
    while pause:
        pause = False if input('Press 0 to continue') == "0" else True
    
    return pause


def create_balanced_dataFrame(sample_number: int, full_dataFrame: pd.DataFrame, configuration)->pd.DataFrame:
        """
    Create a balanced DataFrame by resampling data for each unique label.

    Args:
        sample_number (int): Number of samples to resample for each label.
        full_dataFrame (pd.DataFrame): Full DataFrame containing the data.
        configuration: Configuration object controlling the behavior of the function.

    Returns:
        pd.DataFrame: Balanced DataFrame with resampled data.
    """
        # Extract unique labels from the full DataFrame
        list_of_labels = full_dataFrame['label'].unique()

        # Print unique labels if in debug mode
        if configuration.DEBUG:
            print(f'The List of Unique Labels is:\n \t\t {list_of_labels}')
         
         # Initialize a list to store resampled data for each label
        resampled_data = []
        
        # Iterate over each unique label
        for index, label in enumerate(list_of_labels):
            # Filter data for the current label
            data_row = full_dataFrame[full_dataFrame['label'] == label]
        
            # Resample data to achieve balance
            resampled_data.append(resample(data_row, replace=True, n_samples=sample_number, random_state=configuration.SEED))

        # Concatenate resampled data for all labels into a single DataFrame
        balanced_data = pd.concat(resampled_data, ignore_index=True)

        return balanced_data


def get_user_sample_size(config: configuration):
        sentinel = True
        while sentinel:
            user_scale = input(f'Please enter a number of samples, Leave empty to use default {config.sample_size}') # start with 500
            if user_scale == "":
                sentinel = False
                user_scale = config.sample_size
            elif user_scale.isinstance(int):
                sentinel = False
                return user_scale
            else:
                # if you hit a wrong key or something.
                user_scale = ""
        return user_scale

def create_and_compile_model(configuration):
        
        # # create the model
        # model = Sequential()
        # model.add(Conv2D(256, kernel_size = (3,3), input_shape = (configuration.SIZE[0], configuration.SIZE[1], 3), activation = 'relu', padding = 'same'))
        # model.add(BatchNormalization())
        # model.add(MaxPool2D(pool_size = (2,2)))
        # model.add(Dropout(0.3))

        # model.add(Conv2D(128, kernel_size = (3,3), activation = 'relu'))
        # model.add(MaxPool2D(pool_size = (2,2)))
        # model.add(Dropout(0.3))
        
        # model.add(Conv2D(64, kernel_size = (3,3), activation = 'relu'))
        # model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))
        # model.add(Dropout(0.3))
        # model.add(Flatten())

        # # model.add(Dense(64))
        # model.add(Dense(32))
        # model.add(Dense(7, activation='softmax'))
        # if configuration.DEBUG:
        #      model.summary()
        # model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['acc'])     
        model=Sequential()

        model.add(Conv2D(64,(2,2),input_shape=(28,28,3),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Conv2D(512,(2,2),input_shape=(28,28,3),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Dropout(0.3))

        model.add(Conv2D(1024,(2,2),input_shape=(28,28,3),activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())

        model.add(Dropout(0.3))

        model.add(Conv2D(1024,(1,1),input_shape=(28,28,3),activation='relu'))
        model.add(MaxPooling2D(pool_size=(1, 1)))
        model.add(BatchNormalization())
        #
        model.add(Dropout(0.3))
        model.add(Conv2D(1024,(1,1),input_shape=(28,28,3),activation='relu'))
        model.add(MaxPooling2D(pool_size=(1, 1)))
        model.add(BatchNormalization())

        #
        model.add(Dropout(0.3))

        model.add(Flatten())

        model.add(Dense(256,activation='relu'))
        model.add(Dropout(0.5))


        model.add(Dense(7,activation='softmax'))

        model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['acc'])

        return model


# Where the magic happens.
def main():

    # Initialize configuration object
    configuration = Configuration()

    # Initialize messages object
    messages = Messages()

    # Display welcome message
    messages.welcome_message()

    # Set seed for reproducibility
    np.random.seed(configuration.SEED)

    # Load the metadata into a DataFrame
    skin_dataFrame = pd.read_csv(configuration.ham_csv)
    
    # Convert labels from initials to numbers using LabelEncoder
    label_encoder = LabelEncoder()
    label_encoder.fit(skin_dataFrame['dx'])
    skin_dataFrame['label'] = label_encoder.transform(skin_dataFrame["dx"])

    # Display class counts before transformation if in debug mode
    if configuration.DEBUG:
        messages.show_classes(label_encoder)

    # Display label counts after transformation if in debug mode
    if configuration.DEBUG:
        print(list(skin_dataFrame['label'].value_counts()))

    # Create paths for the images
    image_path = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join('HAM10000/', '*', '*.jpg'))}

    # Add image paths to the DataFrame
    skin_dataFrame['path'] = skin_dataFrame['image_id'].map(image_path.get)

    # Display label counts after adding image paths if in debug mode
    if configuration.DEBUG:
        print(skin_dataFrame['dx'].value_counts())

# -----------------------------------------------------------------------------

    # once done, you have all the photos size corrected and loaded in ram
    process_images_with_progress(configuration, skin_dataFrame)
    if configuration.DEBUG: # ---------- DEBUG
        # Get a little taste, proof of life.
        print(skin_dataFrame.sample(10))    

    # Here we have some choices to make.
    print(messages.loaded_message)
    _next = input(messages.options)

    choosing = True
    while choosing:
    
        # Option 1 -> visualize Data.
        if _next == "1":
            choosing = visualize_our_data(skin_dataFrame)
    
        # Option 2 -> Here we will balance the data.    
        elif _next == "2":
            # First get sample size, default = 500
            sample_size = get_user_sample_size(config=configuration)
            messages.resample_message(sample_size)
            # make a new balanced dataframe, keeping the original in tact.
            balanced_skin_dataFrame = create_balanced_dataFrame(sample_number=sample_size, full_dataFrame=skin_dataFrame, configuration=configuration)
            if configuration.DEBUG: # ---------- DEBUG
                choosing = visualize_our_data(balanced_skin_dataFrame)
            else:
                choosing = False
    
        # Option 3 -> Exit        
        elif _next == "3":
            # bye, bye
            exit()
        else:
            _next = input(messages.options)

    # gotta split the data and fix float issue.
    image_list_array = np.asanyarray(balanced_skin_dataFrame['image'].tolist())
    image_list_array = image_list_array/255
    Y = balanced_skin_dataFrame['label']
    Y_cat = to_categorical(Y, num_classes=7)
    # now Split
    x_train_set, x_test_set, y_train_set, y_test_set = train_test_split(image_list_array, Y_cat, test_size=configuration.train_test_split[1], train_size=configuration.train_test_split[0], random_state=configuration.SEED)


    if configuration.DEBUG:
        print(f'The Training Set Size is:\t {len(x_train_set)} \n It Should be:\t {floor(0.8 * (len(balanced_skin_dataFrame)))}')
        print(f'The Testing DataSet is:\t {len(x_test_set)}\n It Should be:\t {floor(0.8 * (len(balanced_skin_dataFrame)))}')

##----------------------------------------------------------------------------##
 ## NOTE: HERE The Images are loaded,500 of each have been selected randomly## 
##----------------------------------------------------------------------------##
    # x and y train and test sets available here on.
    model = create_and_compile_model(configuration=configuration)

    # Time to Train our model... Finally.
    # this is how many samples it grabs per propagation.
    epochs = configuration.epochs # Times around the data.


    history = model.fit(x_train_set, y_train_set, epochs=epochs, batch_size=configuration.batch_size, class_weight=configuration.class_weights, validation_data=(x_test_set, y_test_set), verbose=2)

    #   save the model
    model.save('ham_cancer_model.h5')
    # save the model in a transportable way.
    tf.saved_model.save(model, 'models')

    # check the final product
    score = model.evaluate(x_test_set, y_test_set)
    print('Test accuracy:', score[1])

    # plot th training and validation accuracy and loss at each epoch.
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, 'y', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()    




# Need this to organize everything
if __name__ == "__main__":
    # Get the party Started.
    main()






