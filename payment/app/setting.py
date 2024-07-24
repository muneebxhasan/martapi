from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")

YOUR_DOMAIN = config("YOUR_DOMAIN", cast=str, default="http://localhost:8006")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=Secret)