from sqlmodel import create_engine
from app import setting
from sqlmodel import Session, select
from app.model.user_model import Userr, UserCreate
from app.crud import user_crud
# connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")

connection_string = str(setting.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

test_connection_string = str(setting.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string, pool_recycle=300 , connect_args={})

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    user = db.exec(
        select(Userr).where(Userr.email == setting.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            email=setting.FIRST_SUPERUSER_EMAIL,
            password=str(setting.FIRST_SUPERUSER_PASSWORD),
            username=setting.FIRST_SUPERUSER_USERNAME,
            full_name=setting.FIRST_SUPERUSER_USERNAME,
            number=1234567890,
            address="paksitan",
            is_superuser=True
        )
        user = user_crud.create_user(user_in,db)





