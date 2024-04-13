import requests

doctors = [
  {
    "email": "taylor.swift@gmail.com",
    "password": "password",
    "firstName": "Taylor",
    "lastName": "Swift",
    "dob": "2001-11-26",
    "medicalLicenseNo": "12345",
    "practice": {
      "name": "West Coast Health",
      "streetAddress": "123 Main St.",
      "city": "Fullerton",
      "state": "CA",
      "zipCode": "92835",
      "telNo": "+1 (949) 123-4560"
    },
    "mobileNo": "+1 (949) 234-5699"
  },
  {
    "email": "jack.smith@gmail.com",
    "password": "password",
    "firstName": "Jack",
    "lastName": "Smith",
    "dob": "1997-01-31",
    "medicalLicenseNo": "98765",
    "practice": {
      "name": "OC Medical Office #2",
      "streetAddress": "456 Main St.",
      "city": "San Juan Capistrano",
      "state": "CA",
      "zipCode": "92676",
      "telNo": "+1 (949) 987-6542"
    }
  }
]

for doctor in doctors:
  response = requests.post("http://localhost/api/doctors", json=doctor)
  print(response.status_code, response.json())

# patients = [
#   {
#     "email": "pete.smith@gmail.com",
#     "password": "password",
#     "firstName": "Pete",
#     "lastName": "Smith",
#     "dob": "2000-01-01",
#     "streetAddress": "123 Main St.",
#     "city": "Orange",
#     "state": "CA",
#     "zipCode": "92835",
#     "mobileNo": "+1 (949) 234-5677"
#   },
# ]

# for patient in patients:
#   response = requests.post("http://localhost/api/patients", json=patient)
#   print(response.status_code, response.json())
