from sqlmodel import Session
from app.core.db_eng import engine

def get_session():
    with Session(engine) as session:
        yield session

