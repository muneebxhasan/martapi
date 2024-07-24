from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.setting import SECRET_KEY, ALGORITHM
from jose import jwt 

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def create_access_token(subject:dict,expires_delta:timedelta):
    to_encode = {"sub":str(subject),"exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode,str(SECRET_KEY),algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


def get_password_hash(password:str):
    return pwd_context.hash(password)