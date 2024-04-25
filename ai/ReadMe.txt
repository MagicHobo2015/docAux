______            ___             
|  _  \          / _ \            
| | | |___   ___/ /_\ \_   ___  __
| | | / _ \ / __|  _  | | | \ \/ /
| |/ / (_) | (__| | | | |_| |>  < 
|___/ \___/ \___\_| |_/\__,_/_/\_\.
Skin Cancer Classification AI Model

Overview

This repository contains an AI model for classifying skin cancer. The model is trained to classify images of skin lesions into different categories of skin cancer.
Usage

    Model: The trained model is available in the model_current directory. Use this model for classification tasks.

    Dependencies Installation:
        To install dependencies via pip, run pip_requirements.install_me.
        To install dependencies via conda, run conda_requirements.install_me.

    Training Your Own Model:
        Use current_model_maker.py to train your own model. The trained model will be saved in the models_in_progress folder.
        Evaluate the trained model using current_model_evaluator.py.

    TensorBoard:
        TensorBoard is utilized to visualize training progress with charts and graphs.
        Start TensorBoard with tensorboard --logdir 'logs/' and access it via localhost:6006.
        View various graphs in the logs folder.

    Checkpoints and Logs:
        Checkpoints from each epoch during training are saved automatically in the check_points directory.
        Previous attempts and models are stored in the old_stuff folder for reference.

Instructions

    Use the provided trained model in model_current for skin cancer classification.
    Install dependencies using either pip_requirements.install_me or conda_requirements.install_me.
    Train your own model using current_model_maker.py, then evaluate it with current_model_evaluator.py.
    Utilize TensorBoard for visualizing training progress.
    Checkpoints and logs are stored for monitoring and reference.


Links
    The link to the dataset organized by class.
    https://drive.google.com/drive/folders/1ZCOZ8X7a_EEIwetus5Z8WtFQrswY1aBZ?usp=sharing



Feel free to explore and contribute to the improvement of the skin cancer classification model!