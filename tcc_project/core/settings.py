from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    DATABASE: str = config('database')
    USER: str = config('user')
    PASSWORD: str = config('password')
    HOST: str = config('host')
    PORT: str = config('port')

settings = Settings()