from sqlmodel import SQLModel, Field



#using noficationapi which store the notification details,so no need for database i guess
class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    notification:str
    user_email: str
    message: str