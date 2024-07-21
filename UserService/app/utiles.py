from fastapi import HTTPException, status
from app import setting
from jose import JWTError, jwt
from app.model.user_model import TokenPayload

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW-Authenticate": 'Bearer'},
    detail={"error": "invalid_token", "error_description": "The access token expired"}
)

def validate_refresh_token(token: str):
    # try:
        secret_key = str(setting.SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=[setting.ALGORITHM])
        payload = TokenPayload(**payload)
        return payload
    # except JWTError:
    #     raise credentials_exception