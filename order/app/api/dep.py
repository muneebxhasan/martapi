from app.core import db_eng
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from app.core import requests
from app import setting
from app.models.order_model import UserInfo


def get_db():
    with Session(db_eng.engine) as session:
        yield session


DB_session =  Annotated[Session,Depends(get_db)]      

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verfiy_current_user_dep(token:Annotated[str|None,Depends(oauth2_scheme)]):
    user = requests.get_current_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # if user.get("disabled",True):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
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
    # if user.get("is_superuser") == False:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    return auth_tokens

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]


