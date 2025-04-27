from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.crud import get_all_cities
from database.engine import AsyncSessionLocal


def start_main_menu_keyboard() -> InlineKeyboardBuilder:

    """

    Основная клавиатура меню для пользователя
    Все основные разделы находятся здесь

    - Сделать заказ
    - Доставка + Оплата заказа
    - Наши филиалы + О нас
    - Частые вопросы

    :return: объект InlineKeyboardBuilder с кнопками
    """

    # создаем объект клавиатуры
    keyboard = InlineKeyboardBuilder()

    # самая первая и длинная кнопка
    keyboard.button(text='Сделать заказ 🛍', callback_data='make_order')

    # остальные кнопки идут по 2 штуки в 1 строке
    keyboard.row(
        InlineKeyboardButton(text='Доставка', callback_data='delivery'),
        InlineKeyboardButton(text='Оплата заказа', callback_data='pay_order'))

    keyboard.row(
        InlineKeyboardButton(text='Наши филиалы', callback_data='branches'),
        InlineKeyboardButton(text='О нас', callback_data='about'))

    keyboard.row(
        InlineKeyboardButton(text='Частые вопросы', callback_data='faq')
    )

    return keyboard


def make_order_keyboard(city_link: str) -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Сделать заказ"

    - За покупками (ссылка на канал)
    - Назад

    :param city_link: пригласительная ссылка на канал для формирования сообщения
    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='За покупками 🛍', url=city_link)
    keyboard.button(text='Назад', callback_data='main_menu')
    keyboard.adjust(1)

    return keyboard


def delivery_keyboard() -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Доставка"

    - Посмотреть пункты выдачи
    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Посмотреть пункты выдачи', callback_data='where_receive')
    keyboard.button(text='Назад', callback_data='main_menu')
    keyboard.adjust(1)
    return keyboard


def pay_order_keyboard() -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Оплата заказа"

    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data='main_menu')
    keyboard.adjust(1)
    return keyboard


def branches_keyboard() -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Наши филиалы"

    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data='faq')
    keyboard.adjust(1)

    return keyboard


def about_keyboard(city_link: str) -> InlineKeyboardBuilder:

    """
    Клавиатура для раздела "О нас"

    - Посмотреть канал
    - Назад

    :param city_link: пригласительная ссылка на канал
    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Посмотреть канал', url=city_link)
    keyboard.button(text='Назад', callback_data='main_menu')
    keyboard.adjust(1)
    return keyboard


async def city_selection_keyboard() -> InlineKeyboardBuilder:

    """
    Клавиатура для выбора города.
    Генерируется клавиатура со всеми городами

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()

    async with AsyncSessionLocal() as session:
        cities = await get_all_cities(session)

    for city in cities:
        keyboard.button(text=cities.get(city), callback_data=f'change_city_{city}')

    keyboard.adjust(1)

    return keyboard


def faq_keyboard() -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Частые вопросы"

    - Связаться с менеджером
    - Когда закупка?
    - Где смотреть цены?
    - Можно поштучно?
    - Где забрать товар?
    - Назад

    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Связаться с менеджером', callback_data='call_manager')

    keyboard.row(
        InlineKeyboardButton(text='Когда закупка?', callback_data='order_schedule'),
        InlineKeyboardButton(text='Где смотреть цены?', callback_data='where_price'),
        InlineKeyboardButton(text='Можно поштучно?', callback_data='min_weigh'),
        InlineKeyboardButton(text='Где забрать товар?', callback_data='where_receive'),
        width=2)

    keyboard.button(text='Назад', callback_data='main_menu')
    keyboard.adjust(1)
    return keyboard


def call_manager_keyboard(manager_url: str) -> InlineKeyboardBuilder:

    """
    Клавиатура меню "Связаться с менеджером"

    - Написать менеджеру
    - Назад

    :param manager_url: ссылка для связи с менеджером
    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Написать менеджеру', url=manager_url)
    keyboard.button(text='Назад', callback_data='faq')
    keyboard.adjust(1)
    return keyboard


def channel_link_keyboard(channel_link: str, back_callback: str) -> InlineKeyboardBuilder:

    """
    Клавиатура для меню, где есть ссылка на канал

    - Перейти в канал
    - Назад

    :param channel_link: ссылка на канал
    :param back_callback: callback для возврата
    :return: объект InlineKeyboardBuilder с кнопками
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Перейти в канал', url=channel_link)
    keyboard.button(text='Назад', callback_data=back_callback)
    keyboard.adjust(1)
    return keyboard


def only_back_button(callback: str = 'main_menu') -> InlineKeyboardBuilder:

    """
    Клавиатура для меню, где только "Назад"

    - Назад

    :param callback: callback для возврата
    :return: объект InlineKeyboardBuilder с кнопкой "Назад"
    """

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data=callback)
    return keyboard
