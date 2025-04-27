from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router
from src.handlers.admin_menu.links_menu.create_link.create_link_menu import create_link_menu

from src.keyboards.links_menu_keyboards import add_link_city_keyboard
from database.engine import AsyncSessionLocal
from database.crud import get_city_by_chat_id

from logs.logger_config import logger


@links_menu_router.callback_query(F.data == 'add_link_city')
async def add_link_city_entering(callback: CallbackQuery):

    """

    Обработка кнопки "Изменить город" (ссылки)
    Переход в меню с выбором города в виде кнопок

    :param callback: callback
    :return:
    """

    # Редактируем сообщение, показываем имя ссылки
    message_text = ''.join(
        (
         'Выберите город / канал',)
    )

    async with AsyncSessionLocal() as session:
        keyboard = await add_link_city_keyboard(session)

    # редактируем сообщение и добавляем новую клавиатуру
    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())


@links_menu_router.callback_query(F.data.startswith('city_'))
async def add_link_city_set(callback: CallbackQuery, state: FSMContext):

    """

    Обработка выбора города из кнопок.
    Внесение значений в state для создания ссылки

    :param callback: callback
    :param state: для записи значений для создания ссылки
    :return:
    """

    async with AsyncSessionLocal() as session:
        city = await get_city_by_chat_id(session, int(callback.data.split('city_')[1]))

    await state.update_data({
        'link_city': city.city
    })

    await create_link_menu(callback, state)
