from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv
load_dotenv()

DATABASE_URL=getenv('DATABASE_URL')
SECRET_KEY=getenv('SECRET_KEY')

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings(DATABASE_URL=DATABASE_URL, SECRET_KEY=SECRET_KEY)
