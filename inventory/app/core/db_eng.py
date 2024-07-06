from sqlmodel import create_engine
from app import settings

# connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

test_connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string, pool_recycle=300 , connect_args={})







