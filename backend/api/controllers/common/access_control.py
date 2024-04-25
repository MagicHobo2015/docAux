from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps

from utils.error_types import DoctorRoleMissingException,\
  PatientRoleMissingException

def doctor_required(fn):
  @wraps(fn)
  @jwt_required()
  def wrapper(*args, **kwargs):
    identity = get_jwt_identity()
    if identity['role'] != 'doctor':
      raise DoctorRoleMissingException
    return fn(*args, **kwargs)
  return wrapper

def patient_required(fn):
  @wraps(fn)
  @jwt_required()
  def wrapper(*args, **kwargs):
    identity = get_jwt_identity()
    if identity['role'] != 'patient':
      raise PatientRoleMissingException
    return fn(*args, **kwargs)
  return wrapper
