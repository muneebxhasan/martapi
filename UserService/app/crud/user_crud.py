from sqlmodel import Session, select    
from fastapi import HTTPException
from typing import Any
from app.model.user_model import Userr, UserCreate, UserUpdate ,UserInfo ,UserRegister
from app.core.security import get_password_hash,verify_password

def get_user_by_email( email: str,db: Session)->UserInfo:
    statement = select(Userr).where(Userr.email == email)
    user = db.exec(statement).first()
    
    return user

def get_user_by_id(user_id: int,db: Session )->UserInfo:
    statement = select(Userr).where(Userr.id == user_id)
    user = db.exec(statement).first()
   
    return user
        
    # user = db.get(Userr,user_id)
    # user = UserInfo(**user.model_dump(exclude={"password"}))
    # return user

def update_user( db_user: Userr, user_in: UserUpdate,session: Session) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_user( user_create: UserRegister,db: Session):
    
    user_create.password = get_password_hash(user_create.password)
    db_user = Userr(**user_create.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user = UserInfo(**db_user.model_dump())
    return user

def update_password(email:str,password:str,db:Session):
    statement = select(Userr).where(Userr.email == email)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    user.password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return {"message":"Password updated successfully"}
    

def authenticate(email:str,password:str,db:Session):
    db_user = get_user_by_email(email,db)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user
    
        
    
