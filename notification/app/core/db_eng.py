from app import setting
from sqlmodel import create_engine


# connection_string = str(setting.DATABASE_URL).replace(
#     "postgresql", "postgresql+pyscopg2")

connection_string = str(setting.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string, connect_args={} , pool_recycle=300)