from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from jsonschema import Draft202012Validator, validate, ValidationError

from api.models import db, Image
from api.controllers.common.access_control import doctor_required
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
@doctor_required
def get_images():
  try:
    doctor_id = get_jwt_identity()['id']
    images = db.session.query(Image).filter_by(doctor_id=doctor_id).all()
    return jsonify([image.image_name for image in images])
  except Exception as e:
    return handle_error(logger, e, 'get_images')

@image_bp.route('/<image_name>', methods=['GET'])
@doctor_required
def get_image(image_name: str):
  try:
    doctor_id = get_jwt_identity()['id']

    image = db.session.query(Image).filter_by(doctor_id=doctor_id, 
                                              image_name=image_name).first()
    if image:
      return jsonify(image.serialize())

    return jsonify({'error': 'Image not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_image')

@image_bp.route('/', methods=['POST'])
@doctor_required
def create_image():
  try:
    doctor_id = get_jwt_identity()['id']
    data = request.get_json()

    validate(instance=data, schema=create_image_schema,
             format_checker=Draft202012Validator)

    image_name = data.get('imageName')
    image_data = data.get('imageData')\

    existing_image = db.session.query(Image)\
      .filter_by(doctor_id=doctor_id, image_name=image_name).first()
    if existing_image:
      return jsonify({'error': 'An image with that name already exists'}), 400

    new_image = Image(doctor_id=doctor_id, image_name=image_name,
                      image_data=image_data)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Image created successfully'}), 201
  except Exception as e:
    if isinstance(e, ValidationError):
      return jsonify({'error': e.message}), 400
    return handle_error(logger, e, 'create_image')

@image_bp.route('/<image_name>', methods=['DELETE'])
@doctor_required
def delete_image(image_name: str):
  try:
    doctor_id = get_jwt_identity()['id']

    image = db.session.query(Image).filter_by(doctor_id=doctor_id, 
                                              image_name=image_name).first()
    if image:
      db.session.delete(image)
      db.session.commit()
      return jsonify({'message': 'Image deleted successfully'})
    
    return jsonify({'error': 'Image not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'delete_image')
