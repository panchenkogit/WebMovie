import os
from dotenv import load_dotenv

env_file = ".env.local"

if os.getenv("ENV") == "docker":
    env_file = ".env.docker"

load_dotenv(dotenv_path=env_file)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URL = os.getenv("REDIS_URL")

ASYNC_DB_URL = os.getenv("ASYNC_DB_URL")
SYNC_DB_URL = os.getenv("SYNC_DB_URL")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))
