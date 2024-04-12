from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from api.models import db, Doctor, Patient, TokenBlocklist
from config.logger import get_logger
from utils.error_utils import handle_error
from utils.password_utils import check_password

logger = get_logger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_user():
  try:
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
      return jsonify({'error': 'Email, password, and role are required'}), 400

    if role not in ['patient', 'doctor']:
      return jsonify({
        'error': '\'role\' must be either \'patient\' or \'doctor\''
      }), 400

    user = None
    if role == 'doctor':
      user = db.session.query(Doctor).filter_by(email=email).first()
    else:
      user = db.session.query(Patient).filter_by(email=email).first()
    
    if user and check_password(password=password, 
                               hashed_password=user.password):
      access_token = create_access_token(identity={
                                           'id': user.id,
                                           'role': role
                                         })
      return jsonify({'accessToken': access_token, 'user': user.serialize()})

    return jsonify({'error': 'Invalid email address or password'}), 401
  except Exception as e:
    return handle_error(logger, e, 'login_user')

@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout_user():
  try:
    jti = get_jwt()['jti']
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({'message': 'User successfully logged out'})
  except Exception as e:
    return handle_error(logger, e, 'logout_user')
