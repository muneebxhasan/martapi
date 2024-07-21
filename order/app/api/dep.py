from app.core import db_eng
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from app.core import requests
from app import setting


def get_db():
    with Session(db_eng.engine) as session:
        yield session


DB_session =  Annotated[Session,Depends(get_db)]      

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{setting.USER_SERVICE_URL}/api/v1/login/access-token")


def get_current_admin_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    user = requests.get_current_user(token)
    if user.get("is_superuser") == False:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

GetCurrentAdminDep = Depends(get_current_admin_dep)

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_tokens = requests.login_for_access_token(form_data)
    # Make a request to get user data and check if user is admin
    user = requests.get_current_user(auth_tokens.get("access_token"))
    if user.get("is_superuser") == False:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return auth_tokens

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]


