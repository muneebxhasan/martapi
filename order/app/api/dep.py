from app.core import db_eng
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

def get_db():
    with Session(db_eng.engine) as session:
        yield session


DB_session =  Annotated[Session,Depends(get_db)]      