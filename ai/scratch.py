# This is for working things out.

#   Current:    Figuring out how to convert predictions into something usefull.
#

import tensorflow as tf
from numpy import argmax
from tensorflow.keras.utils import load_img

def convert_prediction(pred):
    classes_ = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
    log_pred = tf.nn.softmax(pred)

    arg_max = argmax(log_pred)
    pred_con = [classes_[arg_max], log_pred]
    return pred_con


def main():
    model = tf.keras.models.load_model('model_current/')

    # img = load_img('/home/magichobo/development/docAux/ai/images/df/ISIC_0024318.jpg') # df
    
    img = tf.convert_to_tensor(load_img('/home/magichobo/development/docAux/backend/predict_images/smile.jpg')) # smile
    
    img_two = tf.convert_to_tensor(load_img('/home/magichobo/development/docAux/ai/images/vasc/ISIC_0024370.jpg')) # vasc

    new_shape = (-1, img.shape[0], img.shape[1], img.shape[2])
    reshaped_img = tf.reshape(img, new_shape)

    img = img_two
    new_shape = (-1, img.shape[0], img.shape[1], img.shape[2])
    reshaped_img_two = tf.reshape(img, new_shape)
    print(reshaped_img_two.shape)

    prediction_one = model.predict(reshaped_img)
    prediction_two = model.predict(reshaped_img_two)
    # prediction_two = model.predict(reshaped_tensor_two)

    result_one = convert_prediction(prediction_one)
    result_two = convert_prediction(prediction_two)

    print(result_one[1])
    print(result_two[1])
    # print(result_two) # should be Vasc

    # print(f'result_one: {result_one[0]} with a probabibilty of: {result_one[1]}') # should be df



if __name__ == "__main__":
    main()