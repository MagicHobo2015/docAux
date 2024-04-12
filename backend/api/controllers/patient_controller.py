from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,\
  jwt_required
from jsonschema import Draft202012Validator, validate, ValidationError

from api.models import db, Patient, TokenBlocklist
from config.logger import get_logger
from utils.error_utils import handle_error
from utils.password_utils import hash_password

logger = get_logger(__name__)

patient_bp = Blueprint('patient', __name__)

create_patient_schema = {
  'type': 'object',
  'properties': {
    'email': {'type': 'string', 'format': 'email'},
    'password': {'type': 'string'},
    'firstName': {'type': 'string'},
    'lastName': {'type': 'string'},
    'dob': {'type': 'string', 'format': 'date'},
    'streetAddress': {'type': 'string'},
    'city': {'type': 'string'},
    'state': {'type': 'string'},
    'zipCode': {'type': 'string'},
    'mobileNo': {'type': 'string'}
  },
  'required': ['email', 'password', 'firstName', 'lastName', 'dob', 
               'streetAddress', 'city', 'state', 'zipCode', 'mobileNo'],
  'additionalProperties': False
}

@patient_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
  try:
    patients = db.session.query(Patient).all()
    return jsonify([patient.serialize() for patient in patients])
  except Exception as e:
    return handle_error(logger, e, 'get_patients')

@patient_bp.route('/self', methods=['GET'])
@jwt_required()
def get_current_patient():
  try:
    patient_id = get_jwt_identity()['id']
    patient = db.session.query(Patient).get(patient_id)
    if patient:
      return jsonify(patient.serialize())
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_current_patient')

@patient_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
  try:
    patient_id = get_jwt_identity['id']
    patient = db.session.query(Patient).get(patient_id)
    if patient:
      return jsonify([
        notification.serialize() for notification in patient.notifications
      ])
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_notifications')

@patient_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id: int):
  try:
    patient = db.session.query(Patient).get(patient_id)
    if patient:
      return jsonify(patient.serialize())
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_patient')

@patient_bp.route('/', methods=['POST'])
def create_patient():
  try:
    data = request.get_json()

    validate(instance=data, schema=create_patient_schema,
             format_checker=Draft202012Validator.FORMAT_CHECKER)

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    dob = data.get('dob')
    street_address = data.get('streetAddress')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zipCode')
    mobile_no = data.get('mobileNo')

    existing_patient = db.session.query(Patient).filter_by(email=email).first()
    if existing_patient:
      return jsonify({
        'error': 'A user with that email address already exists'
      }), 400

    hashed_password = hash_password(password).decode()
    new_patient = Patient(email=email, password=hashed_password,
                          first_name=first_name, last_name=last_name, dob=dob,
                          street_address=street_address, city=city, state=state,
                          zip_code=zip_code, mobile_no=mobile_no)
    db.session.add(new_patient)
    db.session.commit()
    access_token = create_access_token(identity={
                                         'id': new_patient.id,
                                         'role': 'patient'
                                       })
    return jsonify({
      'accessToken': access_token,
      'user': new_patient.serialize()
    }), 201
  except Exception as e:
    if isinstance(e, ValidationError):
      return jsonify({'error': e.message}), 400
    return handle_error(logger, e, 'create_patient')

@patient_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_patient():
  try:
    patient_id = get_jwt_identity()['id']
    patient = db.session.query(Patient).get(patient_id)
    if patient:
      # Revoke the patient's access token
      jti = get_jwt()['jti']
      now = datetime.now(timezone.utc)
      db.session.add(TokenBlocklist(jti=jti, created_at=now))
      # Delete the patient
      db.session.delete(patient)
      db.session.commit()
      return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'delete_patient')
