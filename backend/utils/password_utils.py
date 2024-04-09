import bcrypt

SALT_ROUNDS = 12

def hash_password(password: str):
  salt = bcrypt.gensalt(rounds=SALT_ROUNDS)
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

def check_password(password: str, hashed_password: str):
  return bcrypt.checkpw(password.encode('utf-8'),
                        hashed_password.encode('utf-8'))
