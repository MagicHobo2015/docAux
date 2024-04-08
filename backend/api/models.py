import base64
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TokenBlocklist(db.Model):
  __tablename__ = 'token_blocklist'
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(36), nullable=False, index=True)
  created_at = db.Column(db.DateTime, nullable=False)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255), nullable=False)
  dob = db.Column(db.Date, nullable=False)
  medical_license_no = db.Column(db.String(255), nullable=False)
  practice_name = db.Column(db.String(255), nullable=False)
  street_address = db.Column(db.String(255), nullable=False)
  city = db.Column(db.String(255), nullable=False)
  state = db.Column(db.String(255), nullable=False)
  zip_code = db.Column(db.String(255), nullable=False)
  tel_no = db.Column(db.String(255), nullable=False)
  mobile_no = db.Column(db.String(255))
  images = db.relationship('Image', backref='user', lazy=True)

  def serialize(self):
    return {
      'id': self.id,
      'email': self.email,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'dob': str(self.dob),
      'medicalLicenseNo': self.medical_license_no,
      'practice': {
        'name': self.practice_name,
        'streetAddress': self.street_address,
        'city': self.city,
        'state': self.state,
        'zipCode': self.zip_code,
        'telNo': self.tel_no
      },
      'mobileNo': self.mobile_no,
      'images': [image.image_name for image in self.images]
    }

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_name = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.BLOB, nullable=False)

    def serialize(self):
      return {
        'imageName': self.image_name,
        'imageData': base64.b64encode(self.image_data).decode()
      }
