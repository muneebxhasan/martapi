from pydantic import ValidationError
from sqlmodel import Session 
from fastapi import Depends , HTTPException
from typing import Annotated
from app.core import db_eng
from app import setting
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from app.model.user_model import TokenPayload, UserInfo, Userr

reusable_oauth2 =  OAuth2PasswordBearer(tokenUrl=f"/user-service{setting.API_STRING}/login/token")

def get_session():
    with Session(db_eng.engine) as session:
        yield session


DB_session =  Annotated[Session,Depends(get_session)]       
TOKEN_dep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(db:DB_session,token: TOKEN_dep)->UserInfo|None:
    try:
        # print("token",token)
        secret_key = str(setting.SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=[setting.ALGORITHM])
        token_data = TokenPayload(**payload)
        # print("token_data",token_data)
    except (JWTError,ValidationError):
        raise HTTPException(status_code=403, detail="Invalid token")
    user = db.get(Userr, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

        
CurrentUser = Annotated[Userr, Depends(get_current_user)]        






