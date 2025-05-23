from pydantic_settings import BaseSettings


class Config(BaseSettings):
    secret_key: str
    jwt_secret_key: str
    sqlalchemy_database_uri: str
    sqlalchemy_track_modifications: bool
    class Config:
        env_file = ".env"

config = Config()
