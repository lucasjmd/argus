from fastapi import Depends, HTTPException, status
from jose import JWTError

from fastapi.security import OAuth2PasswordBearer
from src.api.auth.jwt_token_engine import decode_jwt

# initialising object that extracts the auth token at runtime
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def validate_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extracts and checks if a user has a valid auth token using FastAPI dependency framework.
    Check on presence of token happens before entering the function body.

    Returns the user-id if validated.
    """
    try:
        payload = decode_jwt(token)
        user_id = payload.get('sub')

        if not user_id: # checks for malformed jwt with no user
            raise HTTPException(401, 'Invalid token')

        return user_id

    except JWTError:    # raised if there is a token but it is invalid/expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token'
        )




