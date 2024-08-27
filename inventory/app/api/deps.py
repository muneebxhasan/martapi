from app.core.deps import get_session
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from app.core import requests

DB_session = Annotated[Session,Depends(get_session)]



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# no need as only admin can access the routes
def verfiy_current_user_dep(token:Annotated[str|None,Depends(oauth2_scheme)]):
    user = requests.get_current_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.get("disabled",True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user


GetCurrentUserDep = Annotated[dict, Depends(verfiy_current_user_dep)]

def verify_current_admin_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    user = requests.get_current_user(token) 
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.get("is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user

GetCurrentAdminDep = Depends(verify_current_admin_dep)

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_tokens = requests.login_for_access_token(form_data)
    # Make a request to get user data and check if user is admin
    user = requests.get_current_user(auth_tokens.get("access_token"))
    if user.get("is_superuser") == False:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return auth_tokens

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]


