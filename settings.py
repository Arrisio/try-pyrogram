from pydantic import BaseSettings


class Settings(BaseSettings):
    TG_APP_API_ID: int
    TG_APP_API_HASH: str
    PHONE_NUMBER: str
    TG_2FA_PASSWORD: str

    TG_BOT_TOKEN: str
    TG_BOT_ADMIN_ID: int

    class Config:
        env_file: str = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
