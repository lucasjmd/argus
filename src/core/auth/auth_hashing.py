import bcrypt

def hash_user_password(password: str) -> str:
    """
    Hashes incoming api user passwords for secure storage in database

    :param password: str The user's plain-text password.
    :return: str User's hashed password
    """
    bytes = password.encode('utf-8')
    hashed= bcrypt.hashpw(bytes, bcrypt.gensalt())

    return hashed

def validate_password_attempt(password_attempt: str, stored_password: str) -> bool:
    """
    Compares login attempt password with hashed password

    :param
        - password_attempt: str The user's password attempt
        - stored_password: str The user's stored password

    :return: bool True if passwords match, False otherwise
    """
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, stored_password)

