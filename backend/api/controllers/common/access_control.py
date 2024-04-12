from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from utils.error_types import DoctorRoleMissingException

def require_doctor_role_on_endpoints(bp: Blueprint):
  @bp.before_request
  @jwt_required(optional=True)
  def error_if_user_is_not_doctor():
    identity = get_jwt_identity()
    if identity is not None and identity['role'] != 'doctor':
      raise DoctorRoleMissingException
