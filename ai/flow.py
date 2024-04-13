# This File is made to quickly make and train our model.
import numpy as np
import tensorflow as tf
import datetime
from tensorflow.keras.metrics import Recall
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.layers import Resizing, Rescaling, RandomRotation, Dense, Dropout, Conv2D, RandomFlip, MaxPool2D, Flatten, BatchNormalization, CategoryEncoding
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def create_model(img_size, metrics):
        
        # resizes, rescale, Augmentation: Flips, rotates.. Add: zoom
        preprocessing_layers = [ Resizing( img_size, img_size), Rescaling( 1./255 ), RandomFlip(mode='horizontal_and_vertical'), RandomRotation(factor=0.2, fill_mode='nearest', seed=42) ]


        # create the model
        model = Sequential(preprocessing_layers)
        model.add(Conv2D(256, kernel_size = (3,3), activation = 'relu', input_shape=(None, None,None, 3)))
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
        model.build(input_shape=(None, None,None, 3))
        model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=metrics)
        return model


def main():

    # The directory to pull images from.
    dir = 'images/'
    epochs = 100
    labels = 'inferred'
    c_names = [ 'akiec', 'bcc', 'blk', 'df', 'mel', 'nv', 'vasc' ]
    img_size = 256
    shuffle = True
    seed = 42
    verbose = True
    val_split = .20 # this will be 80% training and 20% validation.
    batch_size = 64 # 32 is a good baseline.
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


    train_ds = image_dataset_from_directory(dir, labels='inferred', validation_split=val_split, subset='training', seed=seed, image_size=( img_size, img_size ), batch_size=batch_size, label_mode='categorical')

    val_ds = image_dataset_from_directory(dir, labels='inferred', label_mode='categorical',validation_split=val_split, subset='validation', seed=seed, image_size=(img_size, img_size), batch_size=batch_size)

    test_dir = 'test_images/'
    test_ds = image_dataset_from_directory(test_dir, labels='inferred', label_mode='categorical', batch_size=batch_size)

    print(test_ds)

    # # tune dataset
    # train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    # val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # model = create_model(img_size=img_size, metrics=metrics)
    # model.summary()

    # def log_confusion_matrix(epoch, logs):
        
    #     test_data = test_ds[0]

    #     # Use the model to predict the values from the validation dataset.
    #     test_pred_raw = model.predict()
    #     test_pred = np.argmax(test_pred_raw, axis=1)

    #     # Calculate the confusion matrix.
    #     cm = confusion_matrix(test_labels, test_pred)
    #     # Log the confusion matrix as an image summary.
    #     figure = plot_confusion_matrix(cm, class_names=class_names)
    #     cm_image = plot_to_image(figure)

    #     # Log the confusion matrix as an image summary.
    #     with file_writer_cm.as_default():
    #         tf.summary.image("epoch_confusion_matrix", cm_image, step=epoch)


    # history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, verbose=1, callbacks=callbacks)

    # model.save('models/')

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