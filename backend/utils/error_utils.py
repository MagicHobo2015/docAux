from flask import jsonify
import logging

def handle_error(logger: logging.Logger, e: Exception, method_name: str, 
                 message='An error occurred', status_code=500):
  logger.error(f'{method_name} caught: {str(e)}')
  return jsonify({'error': message}), status_code
