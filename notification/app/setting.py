from starlette.config import Config
from starlette.datastructures import Secret
from pydantic import (
    computed_field,
)

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
CILENT_ID = config("CILENT_ID", cast=str)
CLIENT_SECRET = config("CLIENT_SECRET", cast=str)    
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_GROUP_ID = config("KAFKA_GROUP_ID", cast=str)

SMTP_HOST = config("SMTP_HOST", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=int)
SMTP_TLS = config("SMTP_TLS", cast=bool)
SMTP_SSL = config("SMTP_SSL", cast=bool)
SMTP_USER = config("SMTP_USER", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=Secret)
EMAILS_FROM_EMAIL = config("EMAILS_FROM_EMAIL", cast=str)
EMAILS_FROM_NAME = config("EMAILS_FROM_NAME", cast=str)


@computed_field  # type: ignore[misc]
@property
def emails_enabled(self) -> bool:
    return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)