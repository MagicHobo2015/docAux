import tensorflow as tf
import numpy as np

def predict(img, model):
    # Reshape image tensor for model input
    reshaped_img = tf.expand_dims(img, axis=0)
    
    # Get raw prediction from model and convert it
    pred = model.predict(reshaped_img)
    return convert_prediction(pred)


def convert_prediction(pred):
    # Convert raw prediction using softmax
    log_pred = tf.nn.softmax(pred)
    
    # Define class labels and corresponding cancer types
    classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
    cancer_types = {
        'nv': 'melanocytic_nevi',
        'mel': 'melanoma',
        'vasc': 'vascular_lesions',
        'df': 'dermatofibroma',
        'bkl': 'benign_keratosis_like_lesions',
        'bcc': 'basal_cell_carcinoma',
        'akiec': 'actinic_keratoses'
    }

    # Initialize results dictionary
    results = {}

    # Populate results with probabilities for each cancer type
    for class_name, cancer_type in cancer_types.items():
        index = classes.index(class_name)
        results[cancer_type] = float(log_pred[0, index])

    # Get the predicted class with the highest probability
    pred_class_index = np.argmax(log_pred)
    results['pred_class'] = classes[pred_class_index]

    return results
