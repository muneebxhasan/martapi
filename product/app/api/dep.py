from sqlmodel import Session 
from fastapi import Depends
from typing import Annotated
from app.core import db_eng

def get_session():
    with Session(db_eng.engine) as session:
        yield session


DB_session =  Annotated[Session,Depends(get_session)]       



