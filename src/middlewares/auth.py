from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.crud import get_user, get_city_link, get_city_by_chat_id, get_city_by_name
from database.engine import AsyncSessionLocal

from logs.logger_config import logger


class AuthMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        pass

    async def __call__(self, handler, event: TelegramObject, data: dict):

        """
        Миддлварь для авторизации пользователя

        Этот миддлварь проверяет, есть ли у пользователя сохраненные данные в состоянии.
        Если данные найдены, пропускает запрос дальше.
        Если данных нет, пытается найти пользователя в базе данных по его user_id,
        затем сохраняет данные о пользователе и городе в состояние.

        - Если пользователь найден в базе данных:
          - Сохраняются данные о пользователе.
          - Сохраняются данные о городе пользователя.
        - Если пользователь не найден:
          - Не выполняется никаких действий, но можно отправить предупреждение.

        :param handler: Обработчик события, которому нужно передать данные.
        :param event: Событие от Telegram, содержащее данные о пользователе.
        :param data: Данные, которые хранятся в состоянии.
        :return: Результат обработки события.
        """

        user_data = await data["state"].get_data()

        if user_data:
            return await handler(event, data)

        user_id = event.from_user.id

        async with AsyncSessionLocal() as session:
            user = await get_user(session, user_id)

            if user:
                # city_link = await get_city_link(session, user.city)
                city = await get_city_by_name(session, user.city)
                await data["state"].update_data(user=user)
                await data["state"].update_data(city=city)
            else:
                # необязательно, но можно — отправить предупреждение
                # await event.answer("Пожалуйста, сначала нажмите /start")
                pass

        return await handler(event, data)
