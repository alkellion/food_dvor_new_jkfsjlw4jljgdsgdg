from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.crud import get_city_by_name, update_user_city, get_user, get_city_by_chat_id
from database.engine import AsyncSessionLocal

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.handlers.user_menu.main.main_menu import user_main_menu


# Обработчик для изменения города пользователя
@user_menu_router.callback_query(F.data.startswith('change_city_'))
async def change_city(callback: CallbackQuery, state: FSMContext):

    """

    :param callback:
    :param state:
    :return:
    """

    city_id = int(callback.data.split('change_city_')[1])

    async with AsyncSessionLocal() as session:
        # Обновляем город пользователя
        city_name = await get_city_by_name(session, city_id)
        await update_user_city(session, callback.from_user.id, city_name)

        # после обновления данных в бд обновляем и в state
        user = await get_user(session, callback.from_user.id)
        city = await get_city_by_chat_id(session, user.city)
        await state.update_data(user=user)
        await state.update_data(city=city)

    await user_main_menu(callback)
    return
