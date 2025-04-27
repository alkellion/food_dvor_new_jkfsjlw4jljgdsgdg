from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from src.states.create_link_states import CreateLinkMenuStates

from config import bot

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router

from src.keyboards.links_menu_keyboards import create_link_menu_keyboard

from logs.logger_config import logger


@links_menu_router.callback_query(F.data == 'create_link_menu')
async def create_link_menu(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки Создать новую ссылку
    Или же вход в меню создания ссылок

    Если ссылку не создали, но вносили значения, они подтянутся из state

    :param callback: callback
    :param state: здесь храним значения для создания ссылки
    :return:
    """

    # достаем данные из состояния
    state_data = await state.get_data()

    # определяем переменные
    link_name = None
    link_city = None
    link_platform = None

    # заполняем переменные из состояния
    if state_data.get('link_name'):
        link_name = state_data.get('link_name')

    if state_data.get('link_city'):
        link_city = state_data.get('link_city')

    if state_data.get('link_platform'):
        link_platform = state_data.get('link_platform')

    # подставляем переменные в сообщение
    message_text = ''.join((
        '<b>Создание отслеживающей ссылки</b> \n\n',
        f'Имя ссылки: <code>{link_name}</code> \n',
        f'Город: <code>{link_city}</code> \n',
        f'Платформа: <code>{link_platform}</code>'
    ))

    # редактируем сообщение, добавляем клавиатуру
    await callback.message.edit_text(message_text, reply_markup=(await create_link_menu_keyboard()).as_markup())
