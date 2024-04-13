from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,\
  jwt_required
from jsonschema import Draft202012Validator, validate, ValidationError

from api.models import db, Doctor, TokenBlocklist
from api.controllers.common.access_control import\
  require_doctor_role_on_endpoints
from config.logger import get_logger
from utils.error_utils import handle_error
from utils.password_utils import hash_password

logger = get_logger(__name__)

doctor_bp = Blueprint('doctor', __name__)
# Set up access control so only doctors can access these endpoints
require_doctor_role_on_endpoints(doctor_bp)

create_doctor_schema = {
  'type': 'object',
  'properties': {
    'email': {'type': 'string', 'format': 'email'},
    'password': {'type': 'string'},
    'firstName': {'type': 'string'},
    'lastName': {'type': 'string'},
    'dob': {'type': 'string', 'format': 'date'},
    'medicalLicenseNo': {'type': 'string'},
    'practice': {
      'type': 'object',
      'properties': {
        'name': {'type': 'string'},
        'streetAddress': {'type': 'string'},
        'city': {'type': 'string'},
        'state': {'type': 'string'},
        'zipCode': {'type': 'string'},
        'telNo': {'type': 'string'},
      },
      'required': ['name', 'streetAddress', 'city', 'state', 'zipCode',
                   'telNo'],
      'additionalProperties': False
    },
    'mobileNo': {'type': 'string'}
  },
  'required': ['email', 'password', 'firstName', 'lastName', 'dob', 
               'medicalLicenseNo', 'practice'],
  'additionalProperties': False
}

@doctor_bp.route('/', methods=['GET'])
@jwt_required()
def get_doctors():
  try:
    doctors = db.session.query(Doctor).all()
    return jsonify([doctor.serialize_basic_info() for doctor in doctors])
  except Exception as e:
    return handle_error(logger, e, 'get_doctors')

@doctor_bp.route('/self', methods=['GET'])
@jwt_required()
def get_current_doctor():
  try:
    doctor_id = get_jwt_identity()['id']
    doctor = db.session.query(Doctor).get(doctor_id)
    if doctor:
      return jsonify(doctor.serialize())
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_current_doctor')

@doctor_bp.route('/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor(doctor_id: int):
  try:
    doctor = db.session.query(Doctor).get(doctor_id)
    if doctor:
      return jsonify(doctor.serialize_basic_info())
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'get_doctor')

@doctor_bp.route('/', methods=['POST'])
def create_doctor():
  try:
    data = request.get_json()

    validate(instance=data, schema=create_doctor_schema,
             format_checker=Draft202012Validator.FORMAT_CHECKER)

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    dob = data.get('dob')
    medical_license_no = data.get('medicalLicenseNo')
    practice = data.get('practice')
    practice_name = practice['name']
    street_address = practice['streetAddress']
    city = practice['city']
    state = practice['state']
    zip_code = practice['zipCode']
    tel_no = practice['telNo']
    mobile_no = data.get('mobileNo')

    existing_doctor = db.session.query(Doctor).filter_by(email=email).first()
    if existing_doctor:
      return jsonify({
        'error': 'A user with that email address already exists'
      }), 400
    
    hashed_password = hash_password(password).decode()
    new_doctor = Doctor(email=email, password=hashed_password,
                        first_name=first_name, last_name=last_name, dob=dob,
                        medical_license_no=medical_license_no,
                        practice_name=practice_name,
                        street_address=street_address, city=city, state=state,
                        zip_code=zip_code, tel_no=tel_no, mobile_no=mobile_no)
    db.session.add(new_doctor)
    db.session.commit()
    access_token = create_access_token(identity={
                                         'id': new_doctor.id,
                                         'role': 'doctor'
                                       })
    return jsonify({
      'accessToken': access_token,
      'user': new_doctor.serialize()
    }), 201
  except Exception as e:
    if isinstance(e, ValidationError):
      return jsonify({'error': e.message}), 400
    return handle_error(logger, e, 'create_doctor')

@doctor_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_doctor():
  try:
    doctor_id = get_jwt_identity()['id']
    doctor = db.session.query(Doctor).get(doctor_id)
    if doctor:
      # Revoke the doctor's access token
      jti = get_jwt()['jti']
      now = datetime.now(timezone.utc)
      db.session.add(TokenBlocklist(jti=jti, created_at=now))
      # Delete the doctor
      db.session.delete(doctor)
      db.session.commit()
      return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
  except Exception as e:
    return handle_error(logger, e, 'delete_doctor')
