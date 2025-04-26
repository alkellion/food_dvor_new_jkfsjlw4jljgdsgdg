from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.crud import get_all_cities
from database.engine import AsyncSessionLocal


async def admin_menu_keyboard():

    """

    :return:
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Меню ссылок', callback_data='links_menu')

    return keyboard
