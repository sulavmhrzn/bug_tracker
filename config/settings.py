from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DEBUG: bool = True
    MONGODB_URL: str
    MONGODB_DB_NAME: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
