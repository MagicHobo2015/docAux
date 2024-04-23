import base64
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from jsonschema import Draft202012Validator, validate, ValidationError

from api.models import db, Image
from config.logger import get_logger
from utils.error_utils import handle_error

logger = get_logger(__name__)

image_bp = Blueprint('image', __name__)

create_image_schema = {
  'type': 'object',
  'properties': {
    'imageName': {'type': 'string'},
    'imageData': {'type': 'string'}
  },
  'required': ['imageName', 'imageData'],
  'additionalProperties': False
}

@image_bp.route('/', methods=['GET'])
@jwt_required()
def get_images():
  try:
    user_id = get_jwt_identity()
    images = db.session.query(Image).filter_by(user_id=user_id).all()
    return jsonify([image.image_name for image in images])
  except Exception as e:
    return handle_error(logger, e, 'get_images')

@image_bp.route('/<image_name>', methods=['GET'])
@jwt_required()
def get_image(image_name: str):
  try:
    user_id = get_jwt_identity()

    image = db.session.query(Image).filter_by(user_id=user_id, 
                                              image_name=image_name).first()
    if image:
      return jsonify(image.serialize())

    return jsonify({'error': 'Image not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_image')

@image_bp.route('/', methods=['POST'])
@jwt_required()
def create_image():
  try:
    user_id = get_jwt_identity()
    data = request.get_json()

    validate(instance=data, schema=create_image_schema,
             format_checker=Draft202012Validator)

    image_name = data.get('imageName')
    image_data = data.get('imageData')
    image_data_bytes = base64.b64decode(image_data)

    existing_image = db.session.query(Image)\
      .filter_by(user_id=user_id, image_name=image_name).first()
    if existing_image:
      return jsonify({'error': 'An image with that name already exists'}), 400

    new_image = Image(user_id=user_id, image_name=image_name,
                      image_data=image_data_bytes)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Image created successfully'}), 201
  except Exception as e:
    if isinstance(e, ValidationError):
      return jsonify({'error': e.message}), 400
    return handle_error(logger, e, 'create_image')

@image_bp.route('/<image_name>', methods=['DELETE'])
@jwt_required()
def delete_image(image_name: str):
  try:
    user_id = get_jwt_identity()

    image = db.session.query(Image).filter_by(user_id=user_id, 
                                              image_name=image_name).first()
    if image:
      db.session.delete(image)
      db.session.commit()
      return jsonify({'message': 'Image deleted successfully'})
    
    return jsonify({'error': 'Image not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'delete_image')
