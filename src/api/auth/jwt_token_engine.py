from jose import jwt, JWTError
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import pytz

load_dotenv()

secret = os.getenv('JWT_SECRET')
expire = os.getenv('JWT_EXPIRY_SECONDS')
algo = os.getenv('JWT_ALGORITHM')

def create_jwt(data: dict) -> str:

    payload = data.copy()

    expiry_dt = datetime.now(pytz.timezone('Europe/Amsterdam'))

    expire_td = timedelta(seconds=int(expire))
    payload['exp'] = expiry_dt + expire_td

    token = jwt.encode(payload, secret, algorithm=algo)

    return token

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, secret, algorithm=algo)

