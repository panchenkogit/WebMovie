import bcrypt

def hash_password(password: str):
    hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    return hash_pass


def check_password(password: str, hash_password: str):
    return bcrypt.checkpw(password.encode(), hash_password)

