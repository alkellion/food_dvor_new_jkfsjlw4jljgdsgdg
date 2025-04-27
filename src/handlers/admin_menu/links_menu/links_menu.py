from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import get_all_cities
from database.engine import AsyncSessionLocal

from .links_menu_router import links_menu_router

from src.keyboards.links_menu_keyboards import links_menu_keyboards


@links_menu_router.callback_query(F.data == 'links_menu')
async def link_menu(callback: CallbackQuery):

    """

    Обработка кнопки Меню ссылок.
    Предполагалось, что работы со ссылками будет много

    :param callback: callback
    :return:
    """

    message_text = ''.join(
        'Сообщение меню ссылок'
    )

    await callback.message.edit_text(message_text, reply_markup=(await links_menu_keyboards()).as_markup())
