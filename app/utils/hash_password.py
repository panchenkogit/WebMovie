import bcrypt

def hash_password(password: str) -> str:
    hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    return str(hash_pass)


def check_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password.encode())

