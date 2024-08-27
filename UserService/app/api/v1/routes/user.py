from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import DB_session,CurrentUser
from typing import Any
from app.core.security import verify_password , get_password_hash
from app.crud import user_crud
from app.model.user_model import (
    UserRegister,UserCreate,UserUpdate,UserInfo,Userr,Message,PasswordUpdate)
from app import setting
import json
from app.core.dp_kafka import Producer

router = APIRouter()



@router.post("/signup")
async def register_user(user_register: UserRegister,db:DB_session,producer:Producer):
    """
    Register a new user
    
    """
    if setting.USERS_OPEN_REGISTRATION:
        raise HTTPException(status_code=403, detail="Open user registration is forbidden on this server")
    
    
    db_user = user_crud.get_user_by_email(user_register.email , db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    
    user = user_crud.create_user(user_register,db)

    user_ ={
        "email" : user.email,
        "full_name" : user.full_name,
        "event" : "user_registered"
    }
    user_  = json.dumps(user_).encode('utf-8')
    await producer.send_and_wait("user_notify",user_)

    return user


@router.get("/me", response_model=UserInfo)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    # print("current_user",current_user)
    return current_user


@router.patch("/me", response_model=UserInfo)
async def update_user_me(
     db: DB_session, user_in: UserUpdate, current_user: CurrentUser,producer:Producer
) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = user_crud.get_user_by_email(user_in.email, db)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    # for key, value in user_data.items():
    #     setattr(current_user, key, value) 


    current_user.sqlmodel_update(user_data)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    user_ ={
        "email" : current_user.email,
        "full_name" : current_user.full_name,
        "event" : "user_updated"
    }
    user_  = json.dumps(user_).encode('utf-8')
    await producer.send_and_wait("user_notify",user_)

    return current_user


@router.patch("/me/password", response_model=Message)
async def update_password_me(
    *, db: DB_session, body: PasswordUpdate, current_user: CurrentUser,producer:Producer
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.old_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.password = hashed_password
    db.add(current_user)
    db.commit()
    user_ ={
        "email" : current_user.email,
        "full_name" : current_user.full_name,
        "event" : "user_password_changed"
    }
    user_  = json.dumps(user_).encode('utf-8')
    await producer.send_and_wait("user_notify",user_)
    return Message(message="Password updated successfully")