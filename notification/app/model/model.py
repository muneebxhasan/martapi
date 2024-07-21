from sqlmodel import SQLModel, Field

class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    message: str