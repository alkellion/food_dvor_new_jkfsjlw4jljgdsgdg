import asyncio
from logs.logger_config import logger
from src.handlers import routers
from config import bot, dp, settings
from src.middlewares.inactivity import InactivityMiddleware
from src.middlewares.auth import AuthMiddleware

from database.engine import init_db


async def main():

    """
    собираем все роутеры и подключаем к диспатчеру
    запуск поллинга

    :return:
    """

    # Подключаем все роутеры
    for router in routers:
        # подключаем к каждому роутеру мидлварь
        router.callback_query.middleware(InactivityMiddleware(timeout=300))
        router.callback_query.middleware(AuthMiddleware())
        router.message.middleware(AuthMiddleware())
        dp.include_router(router)

    # создать бд, если в env поставим true
    if settings.INIT_DB:
        await init_db()

    # Удаляем вебхук, т.к у нас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("🚀 Запуск бота...")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Бот остановлен")
