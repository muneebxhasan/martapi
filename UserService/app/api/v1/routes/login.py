from fastapi import APIRouter, Depends, Form, HTTPException
from app.api.deps import DB_session,CurrentUser
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from app.crud import user_crud
from app.model.user_model import Token
from app.core import security
from typing import Any
from app import setting
from app.utiles import credentials_exception , validate_refresh_token
from datetime import timedelta

router = APIRouter()



@router.post("/login/token")
def login_access_token(db:DB_session,
                       form_data:Annotated[OAuth2PasswordRequestForm , Depends()]):
    """generate access token at login"""
    user = user_crud.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    scopes = form_data.scopes.split() if form_data.scopes else ["read", "write"]
    access_token_expire = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expire = timedelta(minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)
    

    token_data = Token(
        access_token=security.create_access_token(user.id, expires_delta=access_token_expire), # access token with id
        refresh_token=security.create_access_token(user.email, expires_delta=refresh_token_expire), # refresh token with email
        expires_in=(setting.ACCESS_TOKEN_EXPIRE_MINUTES*60),

    )
    print(token_data)
    return token_data



@router.post("/oauth/token", response_model=Token)
def tokens_manager_oauth_codeflow(
    db: DB_session,
    grant_type: str = Form(...),
    refresh_token: Optional[str] = Form(None),
    code: Optional[str] = Form(None)
):
    """
    Token URl For OAuth Code Grant Flow

    Args:
        grant_type (str): Grant Type
        code (Optional[str], optional)
        refresh_token (Optional[str], optional)

    Returns:
        access_token (str)
        token_type (str)
        expires_in (int)
        refresh_token (str)
    """
    # Token refresh flow
    if grant_type == "refresh_token":
        # Check if the refresh token is Present
        if not refresh_token:
            raise credentials_exception
        # Validate the refresh token and client credentials
        user_email = validate_refresh_token(refresh_token)
        user =  user_crud.get_user_by_email(user_email.sub, db)
        
        if not user:
            raise credentials_exception

    # Initial token generation flow
    

    access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)
    print("\n\n settings.ACCESS_TOKEN_EXPIRE_MINUTES \n\n ", setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        refresh_token=security.create_access_token(
            user.email, expires_delta=refresh_token_expires
        ),
        expires_in=(setting.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    )

    print("\n\n token_data \n\n ", token_data)
    return token_data