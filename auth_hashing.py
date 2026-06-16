import bcrypt

def hash_user_password(password: str) -> str:

    bytes = password.encode('utf-8')
    hashed= bcrypt.hashpw(bytes, bcrypt.gensalt())

    return hashed