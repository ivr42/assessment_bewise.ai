from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False
    TASK2_ROOT_PATH: str = ""
    TASK2_APP_DB_NAME: str
    TASK2_APP_DB_USER: str
    TASK2_APP_DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    # maximum attempts to get new questions from jservice.io
    MAX_RETRY: int = 10

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            "postgresql+asyncpg://"
            f"{self.TASK2_APP_DB_USER}:{self.TASK2_APP_DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.TASK2_APP_DB_NAME}"
        )

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
