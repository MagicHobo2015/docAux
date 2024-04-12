import base64
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TokenBlocklist(db.Model):
  __tablename__ = 'token_blocklist'
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(36), nullable=False, index=True)
  created_at = db.Column(db.DateTime, nullable=False)

class PatientNotification(db.Model):
  __tablename__ = 'patient_notifications'
  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.String(512), nullable=False)
  read = db.Column(db.Boolean, nullable=False, server_default='0')
  patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'),
                         nullable=False)

  def serialize(self):
    return {
      'id': self.id,
      'message': self.message
    }

class Patient(db.Model):
  __tablename__ = 'patients'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255), nullable=False)
  dob = db.Column(db.Date, nullable=False)
  street_address = db.Column(db.String(255), nullable=False)
  city = db.Column(db.String(255), nullable=False)
  state = db.Column(db.String(255), nullable=False)
  zip_code = db.Column(db.String(255), nullable=False)
  mobile_no = db.Column(db.String(255), nullable=False)
  notifications = db.relationship('PatientNotification',
                                  backref='notifications',
                                  lazy=True)
  doctor_id = db.Column(db.Integer,
                        db.ForeignKey('doctors.id'))

  def serialize(self):
    patient = {
      'id': self.id,
      'email': self.email,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'dob': str(self.dob),
      'streetAddress': self.street_address,
      'city': self.city,
      'state': self.state,
      'zipCode': self.zip_code,
      'mobileNo': self.mobile_no,
      'notifications': [
        notification.serialize() for notification in self.notifications
      ]
    }
    doctor = self.doctor
    if doctor:
      doctor = doctor.serialize_basic_info()
    patient['doctor'] = doctor
    return patient
  
  def serialize_basic_info(self):
    return {
      'id': self.id,
      'email': self.email,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'dob': str(self.dob),
      'streetAddress': self.street_address,
      'city': self.city,
      'state': self.state,
      'zipCode': self.zip_code,
      'mobileNo': self.mobile_no
    }

class Doctor(db.Model):
  __tablename__ = 'doctors'
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
  images = db.relationship('Image', backref='doctor', lazy=True)
  patients = db.relationship('Patient', backref='doctor', lazy=True)

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
      'images': [image.image_name for image in self.images],
      'patients': [patient.serialize_basic_info() for patient in self.patients]
    }
  
  def serialize_basic_info(self):
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
      'mobileNo': self.mobile_no
    }

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer,
                          db.ForeignKey('doctors.id'),
                          nullable=False)
    image_name = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.BLOB, nullable=False)

    def serialize(self):
      return {
        'imageName': self.image_name,
        'imageData': base64.b64encode(self.image_data).decode()
      }
