import requests

doctors = [
  {
    "email": "ethan.safai@gmail.com",
    "password": "password",
    "firstName": "Ethan",
    "lastName": "Safai",
    "dob": "2001-11-26",
    "medicalLicenseNo": "12345",
    "practice": {
      "name": "West Coast Clinic",
      "streetAddress": "123 Main St.",
      "city": "Fullerton",
      "state": "CA",
      "zipCode": "92835",
      "telNo": "+1 (949) 123-4567"
    },
    "mobileNo": "+1 (949) 234-5678"
  },
  {
    "email": "john.doe@gmail.com",
    "password": "password",
    "firstName": "John",
    "lastName": "Doe",
    "dob": "1997-01-31",
    "medicalLicenseNo": "98765",
    "practice": {
      "name": "OC Medical",
      "streetAddress": "456 Main St.",
      "city": "Dana Point",
      "state": "CA",
      "zipCode": "92629",
      "telNo": "+1 (949) 987-6543"
    }
  }
]

for doctor in doctors:
  response = requests.post("http://localhost/api/doctors", json=doctor)
  print(response.status_code, response.json())

patients = [
  {
    "email": "pete.smith@gmail.com",
    "password": "password",
    "firstName": "Pete",
    "lastName": "Smith",
    "dob": "2000-01-01",
    "streetAddress": "123 Main St.",
    "city": "Orange",
    "state": "CA",
    "zipCode": "92835",
    "mobileNo": "+1 (949) 234-5677"
  },
]

for patient in patients:
  response = requests.post("http://localhost/api/patients", json=patient)
  print(response.status_code, response.json())
