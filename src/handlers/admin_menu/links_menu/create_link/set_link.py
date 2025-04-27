from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from config import bot

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router

from database.crud import db_create_link
from database.engine import AsyncSessionLocal
from logs.logger_config import logger


@links_menu_router.callback_query(F.data == 'create_link')
async def create_link(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки Создать ссылку.
    Собираются все данные, вносятся в бд и возвращают готовую пригласительную ссылку

    :param callback: callback
    :param state: храним данные для создания ссылки
    :return:
    """

    # достаем собранные данные
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

    # достаем имя бота, на котором запущен этот скрипт
    bot_name = (await bot.me()).username

    # подстраиваем собранные значения в ссылку на бота
    link_template = f't.me/{bot_name}?start='

    # подставляем переменные в сообщение
    message_text = ''.join((
        '<b>Создание отслеживающей ссылки</b> \n\n',
        f'Имя ссылки: <code>{link_name}</code> \n',
        f'Город: <code>{link_city}</code> \n',
        f'Платформа: <code>{link_platform}</code> \n\n',
        f'Ссылка создана и сохранена: <code>{link_template}</code>'
    ))

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='В меню ссылок', callback_data='links_menu')

    try:

        async with AsyncSessionLocal() as session:

            result = await db_create_link(session,
                                          state_data['link_name'],
                                          state_data['link_city'],
                                          state_data['link_platform'],
                                          link_template)

            logger.debug(result)

        # result = database.create_link(
        #         state_data['name'],
        #         state_data['city'],
        #         state_data['platform'],
        #         link_template)

        if result == 'name':
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text='Изменить имя', callback_data='insert_name')

            await callback.message.edit_text('Имя ссылки уже есть в базе', reply_markup=keyboard.as_markup())
            return

        # добавляем в базу все значения, которые собрали для ссылки
        if result:
            # подставляем переменные в сообщение
            message_text = ''.join((
                '<b>Создание отслеживающей ссылки</b> \n\n',
                f'Имя ссылки: <code>{link_name}</code> \n',
                f'Город: <code>{link_city}</code> \n',
                f'Платформа: <code>{link_platform}</code> \n\n',
                f'Ссылка создана и сохранена: <code>{result}</code>'
            ))

            # редактируем сообщение
            await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())

            # очищаем из состояния все данные собранные
            await state.clear()

    except KeyError:

        # подставляем переменные в сообщение
        message_text = ''.join((
            '<b>❗️ Заполнены не все значения ❗️</b> \n\n',
            f'Имя ссылки: <code>{link_name}</code> \n',
            f'Город: <code>{link_city}</code> \n',
            f'Платформа: <code>{link_platform}</code> \n'
        ))

        # создаем клавиатуру с кнопками
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text='Изменить имя', callback_data='insert_name')
        keyboard.button(text='Изменить город', callback_data='insert_city')
        keyboard.button(text='Изменить платформу', callback_data='insert_platform')
        keyboard.button(text='Создать ссылку', callback_data='create_link')
        keyboard.button(text='Назад', callback_data='links_menu')

        keyboard.adjust(1)

        await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())
