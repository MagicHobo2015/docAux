# This File is made to quickly make and train our model.
import numpy as np
import tensorflow as tf
import datetime
from tensorflow.keras.metrics import Recall
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.layers import Rescaling, Dense, Dropout, Conv2D, RandomFlip, MaxPool2D, Flatten, BatchNormalization, CategoryEncoding
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import matplotlib.pyplot as plt


def create_model(img_size, metrics):
        
        # create the model
        model = Sequential()
        model.add(CategoryEncoding(num_tokens=7, output_mode='one_hot'))
        model.add( Rescaling( 1./255, input_shape = (img_size, img_size, 3) ))
        model.add( RandomFlip(''))
        model.add(Conv2D(256, kernel_size = (3,3), activation = 'relu'))
        model.add(BatchNormalization())
        model.add(MaxPool2D(pool_size = (2,2)))
        model.add(Dropout(0.3))

        model.add(Conv2D(128, kernel_size = (3,3), activation = 'relu'))
        model.add(MaxPool2D(pool_size = (2,2)))
        model.add(Dropout(0.3))
        
        model.add(Conv2D(64, kernel_size = (3,3), activation = 'relu'))
        model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))
        model.add(Dropout(0.3))
        model.add(Flatten())

        # model.add(Dense(64))
        model.add(Dense(32))
        model.add(Dense(7, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=metrics)
        model.summary()
        return model


def main():

    # The directory to pull images from.
    dir = 'images/'
    epochs = 2
    labels = 'inferred'
    c_names = [ 'akiec', 'bcc', 'blk', 'df', 'mel', 'nv', 'vasc' ]
    img_size = 128
    shuffle = True
    seed = 42
    verbose = True
    val_split = .20 # this will be 80% training and 20% validation.
    batch_size = 32 # 32 is a good baseline.
    # Figures out the best buffer size
    AUTOTUNE = tf.data.AUTOTUNE # automatically, Helps with threadpooling.
    pos_fix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    metrics = ['categorical_accuracy', Recall(),'categorical_crossentropy', 'accuracy']
    auger = None
    # Fit Callbacks.
    tensorboard_callback = TensorBoard(log_dir='logs/' + pos_fix, histogram_freq=1 )
    stop_early = EarlyStopping(monitor='categorical_accuracy',patience=4,mode='auto')
    # Prevents overfitting.
    reduce_lr = ReduceLROnPlateau(monitor='categorical_accuracy', factor=0.5, patience=2, verbose=0,cooldown=0, mode='auto',min_delta=0.0001, min_lr=0)
    # config for checkpoint every epoch. Should switch it to Keep best.
    check_points = ModelCheckpoint('check_points/' + pos_fix, verbose=0, save_freq='epoch')
    # The list to pass to fit.
    callbacks = [check_points, stop_early, reduce_lr, tensorboard_callback]


    train_ds = image_dataset_from_directory(dir, labels='inferred', validation_split=val_split, subset='training', seed=seed, image_size=( img_size, img_size ), batch_size=batch_size)

    val_ds = image_dataset_from_directory(dir, validation_split=val_split, subset='validation', seed=seed, image_size=(img_size, img_size), batch_size=batch_size)

    for batch in train_ds:
        #  print(batch[0].shape)
        #  print(batch[1].shape)
         print(batch[1][0])

    # # tune dataset
    # train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    # val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # model = create_model(img_size=img_size, metrics=metrics)

    # history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, verbose=1, callbacks=callbacks)

    # acc = history.history['accuracy']
    # val_acc = history.history['val_accuracy']

    # loss = history.history['loss']
    # val_loss = history.history['val_loss']

    # epochs_range = range(epochs)

    # plt.figure(figsize=(8, 8))
    # plt.subplot(1, 2, 1)
    # plt.plot(epochs_range, acc, label='Training Accuracy')
    # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    # plt.legend(loc='lower right')
    # plt.title('Training and Validation Accuracy')

    # plt.subplot(1, 2, 2)
    # plt.plot(epochs_range, loss, label='Training Loss')
    # plt.plot(epochs_range, val_loss, label='Validation Loss')
    # plt.legend(loc='upper right')
    # plt.title('Training and Validation Loss')
    # plt.show()


if __name__ == '__main__':
    main()