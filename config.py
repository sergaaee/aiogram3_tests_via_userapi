from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    BOT_CHAT_ID: int
    BOT_TOKEN: str

    class Config:
        env_file = '/home/d10658/PycharmProjects/aiogram3_tests_via_userapi/.env'


def get_settings():
    return Settings()
