from flask import jsonify
import logging

from utils.error_types import DoctorRoleMissingException

def handle_error(logger: logging.Logger, e: Exception, method_name: str, 
                 message='An error occurred', status_code=500):
  logger.error(f'{method_name} caught: {str(e)}')
  if isinstance(e, DoctorRoleMissingException):
    return jsonify({'error': e.message}), 403
  return jsonify({'error': message}), status_code
