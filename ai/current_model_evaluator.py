#        ______            ___             
#       |  _  \          / _ \            
#       | | | |___   ___/ /_\ \_   ___  __
#       | | | / _ \ / __|  _  | | | \ \/ /
#       | |/ / (_) | (__| | | | |_| |>  < 
#       |___/ \___/ \___\_| |_/\__,_/_/\_\.
#       Skin Cancer Classification AI Model


import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory

def evaluate_model(model_dir, images_dir='images/', batch_size=128):
    """
    Evaluate the model using images from the specified directory.

    Args:
        model_dir (str): Directory containing the saved model.
        images_dir (str): Directory containing the evaluation images.
        batch_size (int): Batch size for evaluation.

    Returns:
        dict: Evaluation results including loss and metrics.
    """
    # Load evaluation dataset
    eval_ds = image_dataset_from_directory(
        images_dir,
        labels='inferred',
        label_mode='categorical',
        seed=42,
        batch_size=batch_size
    )

    # Load the saved model
    model = tf.keras.models.load_model(model_dir)

    # Display model summary
    model.summary()

    # Evaluate the model
    results = model.evaluate(eval_ds, verbose=1, return_dict=True)
    print(results)
    return results

def main():
    # Paths
    model_dir = 'models_in_progress'
    images_dir = 'images/'

    # Evaluate the model
    evaluate_model(model_dir, images_dir)

if __name__ == '__main__':
    main()