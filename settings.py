from decouple import config
from pathlib import Path


ABS_PATH = Path().resolve()

KASPI_USERNAME = config("KASPI_USERNAME", cast=str)
KASPI_PASSWORD = config("KASPI_PASSWORD", cast=str)

DB_URL = config("DB_URL", cast=str)

MTPROTO_API_ID = config("MTPROTO_API_ID", cast=str)
MTPROTO_API_HASH = config("MTPROTO_API_HASH", cast=str)
