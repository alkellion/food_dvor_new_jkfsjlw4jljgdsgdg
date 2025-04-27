from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router

from src.keyboards.links_menu_keyboards import links_stat_menu_keyboard

from database.engine import AsyncSessionLocal
from database.crud import get_city_by_channel_id, get_city_links_stat


@links_menu_router.callback_query(F.data == 'links_stat')
async def links_stat_menu(callback: CallbackQuery):

    """

    Обработка кнопки Статистика ссылок

    :param callback: callback
    :return:
    """

    message_text = ''.join(
        'Сообщение меню статистики ссылок по городам')

    async with AsyncSessionLocal() as session:
        keyboard = await links_stat_menu_keyboard(session)

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())


@links_menu_router.callback_query(F.data.startswith('stat_city_'))
async def get_link_stat(callback: CallbackQuery):

    """

    Обработка кнопки города для получения статистики всех его ссылок

    :param callback: callback
    :return:
    """

    async with AsyncSessionLocal() as session:
        city = await get_city_by_channel_id(session, int(callback.data.split('stat_city_')[1]))

        all_links = await get_city_links_stat(session, city.city)

    # создаем список строк для формирования сообщения
    links_stat_message = [f'<b>Статистика ссылок города {city.city}</b> \n\n']

    # перебираем каждую ссылку и формируем сообщение
    for link in all_links:

        users = 0

        if link.users:
            users = len(link.users.split('\n'))

        # создаем темплейт для сообщения и подставляем данные
        message_text = ''.join((
            f'Имя: <code>{link.name}</code> \n',
            f'Платформа: <code>{link.platform}</code> \n',
            f'Пользователей: <code>{users}</code> \n',
            f'Ссылка: <code>{link.link}</code> \n',
            f'Дата: <code>{link.date}</code> \n',
            '➖➖➖➖➖➖➖➖➖➖➖➖ \n\n'
        ))

        # добавляем это как одну строку в список
        links_stat_message.append(message_text)

    # соединяем все строки в одно сообщение
    message_text = ''.join(links_stat_message)

    # добавляем кнопку назад к сообщению
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data='links_menu')

    # редактируем сообщение
    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())
