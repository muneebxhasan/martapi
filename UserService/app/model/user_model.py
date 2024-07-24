from typing import Optional
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str
    email: str = Field(index=True, unique=True)
    full_name: str
    is_superuser: bool = False
    disabled: bool = False
    number: int 
    address: str

class Userr(UserBase,table=True):
    id: Optional[int] = Field(primary_key=True)
    password: str
    

class UserInfo(SQLModel):
    username: str
    id: int
    email: str
    full_name: str
    disabled: bool
    is_superuser: bool
    number: int
    address: str

class UserUpdate(SQLModel):
    email : Optional[str] = None
    full_name: Optional[str] = None
    number: Optional[int] = None
    address: Optional[str] = None


    

class UserCreate(UserBase):
    password: str

class UserRegister(SQLModel):
    email : str
    full_name : str
    password : str  
    username : str  
    number: int 
    address: str
    
class PasswordUpdate(SQLModel):
    old_password: str
    new_password: str


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None
    expires_in: int


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class Message(SQLModel):
    message : str
