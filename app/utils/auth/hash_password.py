import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()

def check_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password.encode())
