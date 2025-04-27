
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from database.models import Base

# достаем из конфига ссылку для подключения к бд
DATABASE_URL = settings.DATABASE_URL_asyncpg

# создаем движок для подключени к бд, выводим что делает бд в консоль
engine = create_async_engine(DATABASE_URL, echo=True)

# делаеv асинхронную сессию для работы
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# запускаем бд и создаем таблицы
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
