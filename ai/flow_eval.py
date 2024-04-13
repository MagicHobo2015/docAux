# This is made to evaluate the model thats created by flow.py
# other models we made may have different encoding for labels
# so these reuslts with them will be incorrect.

import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory

    # train_ds = image_dataset_from_directory(dir, labels='inferred', validation_split=val_split, subset='training', seed=seed, image_size=( img_size, img_size ), batch_size=batch_size, label_mode='categorical')


def main():
    dir = 'images/'
    img_size = ( 128, 128 )

    eval_ds = image_dataset_from_directory(dir, labels='inferred', label_mode='categorical', seed=42, batch_size=128)

    model = tf.keras.models.load_model('models')

    model.summary()
    # loss and metrics, returned here
    results = model.evaluate(eval_ds, verbose=1, return_dict=True )
    print(results)


if __name__ == '__main__':
    main()