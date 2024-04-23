#        ______            ___             
#       |  _  \          / _ \            
#       | | | |___   ___/ /_\ \_   ___  __
#       | | | / _ \ / __|  _  | | | \ \/ /
#       | |/ / (_) | (__| | | | |_| |>  < 
#       |___/ \___/ \___\_| |_/\__,_/_/\_\.
#
#                           Skin Cancer Classification AI Model
#   This file creats a cnn model that classifies skin caner types.

import datetime
import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.metrics import Recall
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Resizing, Rescaling, RandomRotation, Dense, Dropout, Conv2D, RandomFlip, MaxPool2D, Flatten, BatchNormalization
import matplotlib.pyplot as plt

def create_model(img_size, metrics):
    # Define preprocessing layers
    preprocessing_layers = [
        Resizing(img_size, img_size),
        Rescaling(1. / 255),
        RandomFlip(mode='horizontal_and_vertical'),
        RandomRotation(factor=0.2, fill_mode='nearest', seed=42)
    ]
    # Build the model
    model = Sequential(preprocessing_layers)
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu', input_shape=(None, None, None, 3)))
    model.add(BatchNormalization())
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(32))
    model.add(Dense(7, activation='softmax'))
    model.build(input_shape=(None, None, None, 3))
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=metrics)
    return model

def prepare_datasets(dir='images/', test_dir='test_images/', val_split=0.20, batch_size=128):
    # Load training dataset
    train_ds = image_dataset_from_directory(
        dir,
        labels='inferred',
        validation_split=val_split,
        subset='training',
        seed=42,
        image_size=(128, 128),
        batch_size=batch_size,
        label_mode='categorical'
    )
    # Load validation dataset
    val_ds = image_dataset_from_directory(
        dir,
        labels='inferred',
        validation_split=val_split,
        subset='validation',
        seed=42,
        image_size=(128, 128),
        batch_size=batch_size,
        label_mode='categorical'
    )
    # Load test dataset
    test_ds = image_dataset_from_directory(
        test_dir,
        labels='inferred',
        batch_size=batch_size,
        label_mode='categorical'
    )
    # Concatenate train and test datasets
    train_ds = train_ds.concatenate(test_ds)
    # Cache and prefetch datasets for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return train_ds, val_ds

def main():
    # Configuration
    dir = 'images/'
    test_dir = 'test_images/'
    epochs = 75
    img_size = 128
    val_split = 0.20
    batch_size = 128
    metrics = ['categorical_accuracy', Recall(), 'categorical_crossentropy', 'accuracy']
    pos_fix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Define callbacks for training
    tensorboard_callback = TensorBoard(log_dir=f'logs/{pos_fix}', histogram_freq=1)
    stop_early = EarlyStopping(monitor='categorical_accuracy', patience=4, mode='auto')
    reduce_lr = ReduceLROnPlateau(monitor='categorical_accuracy', factor=0.5, patience=2, verbose=0, cooldown=0, mode='auto', min_delta=0.0001, min_lr=0)
    check_points = ModelCheckpoint(f'check_points/{pos_fix}', verbose=0, save_freq='epoch')
    callbacks = [check_points, stop_early, reduce_lr, tensorboard_callback]

    # Prepare datasets
    train_ds, val_ds = prepare_datasets(dir, test_dir, val_split, batch_size)

    # Create and summarize the model
    model = create_model(img_size, metrics)
    model.summary()
    
    # Train the model
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, verbose=1, callbacks=callbacks)

    # Save the trained model
    model.save('models/')

    # Extract metrics from training history
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

if __name__ == '__main__':
    main()
