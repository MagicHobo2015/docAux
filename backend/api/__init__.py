from datetime import timedelta
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy import text

from config.logger import get_logger
from api.models import db, TokenBlocklist
from api.controllers.auth_controller import auth_bp
from api.controllers.doctor_controller import doctor_bp
from api.controllers.image_controller import image_bp
from api.controllers.notification_controller import notification_bp
from api.controllers.patient_controller import patient_bp
from utils.error_types import DoctorRoleMissingException,\
  PatientRoleMissingException
from utils.error_utils import handle_error

logger = get_logger(__name__)

#-------------------------------------------------------------------------------
# Private methods
#-------------------------------------------------------------------------------

def _load_env_variables():
  try:
    load_dotenv('.env')
  except FileNotFoundError:
    logger.info('Oops! .env file missing')
    exit(1)

def _initialize_flask_app():    
  app = Flask(__name__)
  # So the orm can find the db
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =\
    os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
  # Add jwt auth to app
  app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  return app

def _check_token_in_blocklist(_, jwt_payload: dict) -> bool:
  jti = jwt_payload["jti"]
  token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).first()
  return token is not None

def _add_jwt_auth(app: Flask):
  jwt = JWTManager()
  jwt.token_in_blocklist_loader(_check_token_in_blocklist)
  jwt.init_app(app)

def _connect_database(app: Flask):
  db.init_app(app)
  with app.app_context():
    try:
      # db.drop_all()
      db.create_all()
      db.session.execute(text('SELECT 1'))
      logger.info('Database connection successful')
    except Exception as e:
      logger.error(f'Database connection failed! ERROR: {str(e)}')

def _configure_cors_if_dev(app: Flask):
  if os.environ['RUN_MODE'] == 'debug':
    CORS(app)

def _setup_routes(app: Flask):
  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
  app.register_blueprint(image_bp, url_prefix='/api/images')
  app.register_blueprint(notification_bp, url_prefix='/api/notifications')
  app.register_blueprint(patient_bp, url_prefix='/api/patients')

#-------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------

def create_flask_app():
  _load_env_variables()
  app = _initialize_flask_app()
  _configure_cors_if_dev(app)
  _connect_database(app)
  _add_jwt_auth(app)
  _setup_routes(app)
  @app.errorhandler(DoctorRoleMissingException)
  def handle_doctor_role_missing_error(e: DoctorRoleMissingException):
    return handle_error(logger=logger, e=e,
                        method_name='handle_doctor_role_missing_error',
                        message='You are unauthorized to access this resource',
                        status_code=403)
  @app.errorhandler(PatientRoleMissingException)
  def handle_patient_role_missing_error(e: PatientRoleMissingException):
    return handle_error(logger=logger, e=e,
                        method_name='handle_patient_role_missing_error',
                        message='You are unauthorized to access this resource',
                        status_code=403)
  return app
