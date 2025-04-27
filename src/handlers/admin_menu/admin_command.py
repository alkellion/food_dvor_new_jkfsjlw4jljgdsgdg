from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.handlers.admin_menu.admin_menu_router import admin_menu_router
from src.keyboards.admin_menu_keyboards import admin_menu_keyboard
from config import settings


@admin_menu_router.message(Command('admin'), F.from_user.id == settings.ADMIN_ID)
async def admin_start_command(message: Message):

    """

    Обработка команды /admin
    Хотел реализовать через /start по id пользователя
    Но оставил пока так, т.к. прототип

    :param message: message
    :return:
    """

    message_text = ''.join(
        'Сообщение админ панели'
    )

    # отправляем сообщение админ панели с кнопками
    await message.answer(message_text, reply_markup=(await admin_menu_keyboard()).as_markup())


@admin_menu_router.callback_query(F.data == 'admin_menu', F.from_user.id == settings.ADMIN_ID)
async def admin_menu(callback: CallbackQuery):

    """

    То же самое, что и обработка команды, только через callback

    :param callback: callback
    :return:
    """

    message_text = ''.join(
        'Сообщение админ панели'
    )

    # отправляем сообщение админ панели с кнопками
    await callback.message.edit_text(message_text, reply_markup=(await admin_menu_keyboard()).as_markup())

