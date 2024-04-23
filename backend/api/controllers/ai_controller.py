import base64
import tensorflow as tf
from numpy import argmax
from config.logger import get_logger
from config.ai_model import get_ai_model
from utils.error_utils import handle_error
from utils.ai_utils import predict
from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request
from PIL import Image
import io
import numpy as np

# Initialize logger
logger = get_logger(__name__)

# Blueprint for AI routes
ai_bp = Blueprint('ai', __name__)

# Load AI model
model = get_ai_model()

# Endpoint for making predictions
@ai_bp.route('/', methods=['POST'])
@jwt_required
def create_prediction():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Extract image name and base64-encoded image data
        img_name = data.get('imageName')
        b64_bytes = data.get('imageData')

        # Decode base64-encoded image data and open image
        img_decoded = base64.b64decode(b64_bytes.encode())
        img = Image.open(io.BytesIO(img_decoded))
        
        # Ensure image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert image to TensorFlow tensor
        img_tensor = tf.convert_to_tensor(img)

        # Get prediction for the image
        pred = predict(img_tensor, model=model)
        # Just adding the name to the results.
        pred['img_name'] = img_name
        # Return success response
        return jsonify(pred), 200 

    except Exception as e:
        # If an error occurs, handle it
        return handle_error(logger=logger, e=e, method_name='predict')

