import tensorflow as tf
from config.logger import get_logger
from utils.error_utils import handle_error


# get logger, for error reporting.
logger = get_logger(__name__)
_ai_model_dir = '/home/magichobo/development/docAux/ai/model_current'
_ai_model = None

# Just a lonely helper function to load an ai model.
def get_ai_model():
    if _ai_model:
        return _ai_model
    else:
        try:
            _model = tf.keras.models.load_model(_ai_model_dir)
            logger.info('AI model has been mounted successfully.')
            return _model
        except Exception as _e:
            return handle_error(logger, _e, 'get_ai_model', 'There was a problem mounting the ai model' ), 501
