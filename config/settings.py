from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
