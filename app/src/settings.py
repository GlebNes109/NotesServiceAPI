from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    server_port: str
    server_host: str
    class Config:
        env_file = ".env"

settings = Settings()