from pydantic import BaseSettings


class Settings(BaseSettings):
    API_ID:int
    API_HASH: str

    class Config:
        env_file: str = ".env"
        env_file_encoding = "utf-8"

settings = Settings()