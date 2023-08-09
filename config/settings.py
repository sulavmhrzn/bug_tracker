from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DEBUG: bool = True
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
