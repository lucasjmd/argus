from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import pytz

load_dotenv()

secret = os.getenv('JWT_SECRET')
expire = os.genenv('JWT_EXPIRY_SECONDS')
algo = os.getenv('JWT_ALGORITHM')

def create_jwt(data: dict) -> str:

    expiry_dt = datetime.now(pytz.timezone('Europe/Amsterdam'))

    data['exp'] = expiry_dt

    token = jwt.encode(data, secret, algorithm=algo)

    return token

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, secret, algorithm=algo)

