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
import requests
router = APIRouter()



@router.post("/login/token")
def login_access_token(
    db: DB_session, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Generate access token at login"""
    user = user_crud.authenticate(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expire = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expire = timedelta(minutes=setting.REFRESH_TOKEN_EXPIRE_MINUTES)

    token_data = Token(
        access_token=security.create_access_token(user.id, expires_delta=access_token_expire),
        refresh_token=security.create_access_token(user.email, expires_delta=refresh_token_expire),
        expires_in=(setting.ACCESS_TOKEN_EXPIRE_MINUTES * 60),
    )

    # Return the token data along with user_id and email
    return {
        **token_data.dict(),
        "user_id": user.id,
        "email": user.email,
    }




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
    # print("\n\n settings.ACCESS_TOKEN_EXPIRE_MINUTES \n\n ", setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        refresh_token=security.create_access_token(
            user.email, expires_delta=refresh_token_expires
        ),
        expires_in=(setting.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    )

    # print("\n\n token_data \n\n ", token_data)
    return token_data


@router.post("/gpts/oauth/token", response_model=Token)
def gpts_oauth_token_flow(
    grant_type: str = Form(...),
    code: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
    client_id: str = Form(...),  # Client ID specific to GPT-based actions
    client_secret: str = Form(...),  # Client Secret for GPT-based actions
    redirect_uri: str = Form(...),  # Redirect URI for the GPT OAuth flow
    token_url: str = Form(...),  # The GPT-specific Token URL
    scope: Optional[str] = Form(""),  # Scopes specific to GPT API access
):
    """
    Custom OAuth Token URL Handler for GPTs
    This is customized for handling OAuth flows specific to GPT-based actions.

    Args:
        grant_type (str): Can be "authorization_code" or "refresh_token"
        code (Optional[str], optional): Authorization code for exchange
        refresh_token (Optional[str], optional): Refresh token for token refresh
    Returns:
        access_token (str): Generated access token
        refresh_token (str): Generated refresh token
    """
    if grant_type == "authorization_code":
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code required")

        # Exchange authorization code for access token
        token_response = requests.post(
            token_url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': scope,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")

        token_data = token_response.json()

    elif grant_type == "refresh_token":
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")

        # Exchange refresh token for a new access token
        token_response = requests.post(
            token_url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': scope,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange refresh token")

        token_data = token_response.json()

    else:
        raise HTTPException(status_code=400, detail="Unsupported grant type")

    # Validate the token data structure and return it
    if 'access_token' not in token_data:
        raise HTTPException(status_code=400, detail="Access token not found in the response")

    # Return the token data (access_token, refresh_token, etc.)
    return {
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token", ""),
        "expires_in": token_data.get("expires_in", 3600),
        "token_type": token_data.get("token_type", "Bearer")
    }
