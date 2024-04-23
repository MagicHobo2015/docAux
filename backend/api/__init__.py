from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy import text

from config.logger import get_logger
from api.models import db, TokenBlocklist
from api.controllers.ai_controller import ai_bp
from api.controllers.user_controller import user_bp
from api.controllers.auth_controller import auth_bp
from api.controllers.image_controller import image_bp

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
  app.config['AI_MODEL_DIR'] = os.environ['AI_MODEL_DIR']
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

def _setup_routes(app: Flask):
  # app.register_blueprint(user_bp, url_prefix='/api/users')
  app.register_blueprint(user_bp, url_prefix='/api/patients')
  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(image_bp, url_prefix='/api/images')
  app.register_blueprint(ai_bp, url_prefix='/api/predictions')

#-------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------

def create_flask_app():
  _load_env_variables()
  app = _initialize_flask_app()
  _connect_database(app)
  _add_jwt_auth(app)
  _setup_routes(app)
  return app
