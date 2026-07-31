from jose import jwt, JWTError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

#JWT configuration settings from environment
SECRET = os.getenv('JWT_SECRET') # cryptographic signature key
EXPIRE = os.getenv('JWT_EXPIRY_SECONDS')
ALGO = os.getenv('JWT_ALGORITHM')

def create_jwt(data: dict) -> str:
    """
    Generates a JWT by hashing the user-id and expiry timestamp.

    :param data: Dictionary containing user claim
    :return: Encoded JWT as string
    """

    payload = data.copy()
    # opted for UTC to avoid timezone token issues
    expiry_dt = datetime.now(timezone.utc)

    expire_td = timedelta(seconds=int(EXPIRE))
    payload['exp'] = expiry_dt + expire_td

    token = jwt.encode(payload, SECRET, algorithm=ALGO)

    return token

def decode_jwt(token: str) -> dict:
    """
    Decodes incoming JWT and verifies it matches backend signature after rehashing
    incoming header and payload

    :param token: Raw incoming JWT string
    :return: Decoded payload dictionary containing userid
    :raises JWTError: If signature doesnt match
    """
    return jwt.decode(token, SECRET, algorithms=[ALGO])

