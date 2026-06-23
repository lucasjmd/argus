from fastapi import Depends, HTTPException, status
from jose import JWTError

from fastapi.security import OAuth2PasswordBearer
from src.api.auth.jwt_token_engine import decode_jwt

# create token extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def validate_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token)
        user_id = payload.get('sub')

        if not user_id:
            raise HTTPException(401, 'Invalid token')

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token'
        )




