from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_NAME: str
    APP_VERSION: str
    SECRET_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int

    FILE_DEFAULT_CHUNK_SIZE: int

    # class config():
    #     env_file = ".env"


    # class config():
    #     env_file = ".env"


def get_setting():
    return Settings()

