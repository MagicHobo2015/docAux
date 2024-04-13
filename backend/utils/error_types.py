class DoctorRoleMissingException(Exception):
  message = 'Only doctors may perform this action'

  def __str__(self) -> str:
    return self.message

class PatientRoleMissingException(Exception):
  message = 'Only patients may perform this action'

  def __str__(self) -> str:
    return self.message
