from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
API_STRING = config("API_STRING", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=Secret)
USERS_OPEN_REGISTRATION = config("USERS_OPEN_REGISTRATION", cast=bool)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)

FIRST_SUPERUSER_USERNAME = config("FIRST_SUPERUSER_USERNAME", cast=str)
FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD", cast=Secret)
FIRST_SUPERUSER_EMAIL = config("FIRST_SUPERUSER_EMAIL", cast=str)