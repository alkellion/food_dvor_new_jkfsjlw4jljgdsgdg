from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.crud import get_all_cities, get_platforms
from database.engine import AsyncSessionLocal


async def links_menu_keyboards():

    """
    Клавиатура меню ссылок
    Выравнивание по 1 кнопке

    - Создать новую ссылку
    - Статистика ссылок
    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Создать новую ссылку ✍️', callback_data='create_link_menu')
    keyboard.button(text='Статистика ссылок', callback_data='links_stat')
    keyboard.button(text='Назад', callback_data='admin_menu')

    keyboard.adjust(1)

    return keyboard


async def create_link_menu_keyboard():

    """
    Клавиатура меню Создания ссылки

    - Изменить имя
    - Изменить город
    - Изменить платформу
    - Создать ссылку
    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    # создаем клавиатуру с кнопками
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Изменить имя', callback_data='add_link_name')
    keyboard.button(text='Изменить город', callback_data='add_link_city')
    keyboard.button(text='Изменить платформу', callback_data='add_link_platform')
    keyboard.button(text='Создать ссылку', callback_data='create_link')
    keyboard.button(text='Назад', callback_data='links_menu')

    keyboard.adjust(1)

    return keyboard


async def links_stat_menu_keyboard(session):

    """
    Клавиатура с выбором города для получения статистики ссылок по нему
    Из бд достаются все города и создаются кнопки с callback_data = 'stat_city_{city_name}'

    :param session: сессия для работы с бд
    :return: объект InlineKeyboardBuilder с кнопками
    """

    # достаем города из базы
    cities = await get_all_cities(session)

    keyboard = InlineKeyboardBuilder()

    # из данных собираем кнопки
    for city in cities:
        keyboard.button(text=cities.get(city), callback_data=f'stat_city_{city}')

    keyboard.button(text='Назад', callback_data='links_menu')

    # добавляем необходимые кнопки
    keyboard.adjust(1)

    return keyboard


async def add_link_city_keyboard(session):

    """
    Клавиатура с добавлением города к ссылке, либо выход назад.
    Создается клавиатура выбора города для добавления к отслеживающей ссылке

    :param session: сессия для работы с бд
    :return: объект InlineKeyboardBuilder с кнопками
    """

    # клавиатура если нужно изменить имя ссылки или выйти
    keyboard = InlineKeyboardBuilder()

    # достаем города из базы
    cities = await get_all_cities(session)

    # из данных собираем кнопки
    for city in cities:
        keyboard.button(text=cities.get(city), callback_data=f'city_{city}')

    # добавляем необходимые кнопки
    keyboard.button(text='Назад', callback_data='create_link_menu')
    keyboard.adjust(1)

    return keyboard


async def add_link_platform_keybaord(session):

    """
    Клавиатура с добавлением платформы к отслеживающей ссылке.
    Из бд достаются все платформы и генерируется клавиатура


    :param session: сессия для работы с бд
    :return: объект InlineKeyboardBuilder с кнопками
    """

    # клавиатура если нужно изменить имя ссылки или выйти
    keyboard = InlineKeyboardBuilder()

    # достаем города из базы
    platforms = await get_platforms(session)

    # из данных собираем кнопки
    for platform in platforms:
        keyboard.button(text=platforms.get(platform), callback_data=f'platform_{platform}')

    # добавляем необходимые кнопки
    keyboard.button(text='Назад', callback_data='create_link_menu')
    keyboard.adjust(1)

    return keyboard
