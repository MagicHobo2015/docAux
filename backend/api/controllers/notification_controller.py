from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from jsonschema import Draft202012Validator, validate, ValidationError

from api.models import db, Patient, PatientNotification
from api.controllers.common.access_control import doctor_required
from config.logger import get_logger
from utils.error_utils import handle_error

logger = get_logger(__name__)

notification_bp = Blueprint('notification', __name__)

create_notification_schema = {
  'type': 'object',
  'properties': {
    'message': {'type': 'string'}
  },
  'required': ['message'],
  'additionalProperties': False
}

@notification_bp.route('/<int:patient_id>', methods=['POST'])
@doctor_required
def add_patient_notification(patient_id: int):
  try:
    data = request.get_json()

    validate(instance=data, schema=create_notification_schema,
             format_checker=Draft202012Validator.FORMAT_CHECKER)

    message = data.get('message')
    message = message.strip()
    if len(message) == 0:
      return jsonify({'error': 'Please provide a notification message'}), 400

    patient = db.session.query(Patient).get(patient_id)
    if patient is None:
      return jsonify({'error': 'Patient not found'}), 404

    doctor_id = get_jwt_identity()['id']
    if patient.doctor_id != doctor_id:
      return jsonify({'error': 'This patient is not assigned to you'}), 403


    notification = PatientNotification(patient_id=patient.id, message=message)
    db.session.add(notification)
    db.session.commit()

    return jsonify({'message': 'Notification created successfully'})
  except Exception as e:
    if isinstance(e, ValidationError):
      return jsonify({'error': e.message}), 400
    return handle_error(logger, e, 'add_patient_notification')
