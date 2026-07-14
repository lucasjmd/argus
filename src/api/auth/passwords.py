import bcrypt

def hash_user_password(password: str) -> str:
    """
    Hashes incoming api user passwords for secure storage in database

    :param password: str The user's plain-text password.
    :return: str User's hashed password
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    hashed_str = hashed_bytes.decode('utf-8')

    return hashed_str

def validate_password_attempt(password_attempt: str, stored_password: str) -> bool:
    """
    Compares login attempt password with hashed password

    :param
        - password_attempt: str The user's plain password attempt
        - stored_password: str The user's encoded stored password

    :return: bool True if passwords match, False otherwise
    """

    stored_password_bytes = stored_password.encode('utf-8')
    attempt_bytes = password_attempt.encode('utf-8')

    return bcrypt.checkpw(attempt_bytes, stored_password_bytes)

