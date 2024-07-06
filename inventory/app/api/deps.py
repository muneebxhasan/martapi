from app.core.deps import get_session
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

DB_session = Annotated[Session,Depends(get_session)]
