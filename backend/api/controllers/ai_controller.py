import tensorflow as tf
from flask import Blueprint
from flask_jwt_extended import jwt_required
from config.logger import get_logger


logger = get_logger(__name__)
ai_bp = Blueprint('ai', __name__)

model = 

@ai_bp.route('/', method=['POST'])
@jwt_required
def predict():
    pass