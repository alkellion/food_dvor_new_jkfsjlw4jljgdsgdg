from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    """
    Класс для настройки конфигурации бота и базы данных.
    Данные берем из .env

    Параметры:
    - TEST_BOT_TOKEN: Токен бота для
    - ADMIN_ID: Админ пока только я
    - INIT_DB: Флаг для инициализации бд
    - DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME: Параметры подключения к базе данных.

    :return: Объект конфигурации с настройками бота и базы данных.
    """

    TEST_BOT_TOKEN: str
    ADMIN_ID: int

    INIT_DB: bool = False

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

# Создаём бота и диспетчер
bot: Bot = Bot(token=settings.TEST_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp: Dispatcher = Dispatcher()
