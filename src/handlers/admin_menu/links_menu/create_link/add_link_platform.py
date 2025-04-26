from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router
from src.handlers.admin_menu.links_menu.create_link.create_link_menu import create_link_menu

from src.keyboards.links_menu_keyboards import add_link_platform_keybaord

from database.engine import AsyncSessionLocal
from database.crud import get_platform

from logs.logger_config import logger


@links_menu_router.callback_query(F.data == 'add_link_platform')
async def insert_platform(callback: CallbackQuery, state: FSMContext):
    # Редактируем сообщение, показываем имя ссылки
    message_text = ''.join(
        (
            'Выберите платформу',)
    )

    async with AsyncSessionLocal() as session:
        keyboard = await add_link_platform_keybaord(session)

    # редактируем сообщение и добавляем новую клавиатуру
    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())


@links_menu_router.callback_query(F.data.startswith('platform_'))
async def insert_platform_callback(callback: CallbackQuery, state: FSMContext):

    async with AsyncSessionLocal() as session:
        platform = await get_platform(session, int(callback.data.split('platform_')[1]))

    await state.update_data({
        'link_platform': platform
    })

    await create_link_menu(callback, state)
