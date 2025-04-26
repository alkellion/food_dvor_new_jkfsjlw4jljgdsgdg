from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.crud import get_all_cities
from database.engine import AsyncSessionLocal


class MainMenuKeyboards:
    @staticmethod
    def start() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Сделать заказ 🛍', callback_data='make_order')
        kb.row(
            InlineKeyboardButton(text='Доставка', callback_data='delivery'),
            InlineKeyboardButton(text='Оплата заказа', callback_data='pay_order')
        )
        kb.row(
            InlineKeyboardButton(text='Наши филиалы', callback_data='branches'),
            InlineKeyboardButton(text='О нас', callback_data='about')
        )
        kb.row(
            InlineKeyboardButton(text='Частые вопросы', callback_data='faq')
        )
        return kb

    @staticmethod
    def make_order(city_link: str) -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='За покупками 🛍', url=city_link)
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb


class InfoKeyboards:
    @staticmethod
    def delivery() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Посмотреть пункты выдачи', callback_data='where_receive')
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb

    @staticmethod
    def pay_order() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb

    @staticmethod
    def branches() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb

    @staticmethod
    def about(city_link: str) -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Посмотреть канал', url=city_link)
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb


class FAQKeyboards:
    @staticmethod
    def faq() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Связаться с менеджером', callback_data='call_manager')
        kb.row(
            InlineKeyboardButton(text='Когда закупка?', callback_data='order_schedule'),
            InlineKeyboardButton(text='Где смотреть цены?', callback_data='where_price'),
            InlineKeyboardButton(text='Можно поштучно?', callback_data='min_weigh'),
            InlineKeyboardButton(text='Где забрать товар?', callback_data='where_receive'),
            width=2
        )
        kb.button(text='Назад', callback_data='start_menu')
        kb.adjust(1)
        return kb

    @staticmethod
    def call_manager(manager_url: str) -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Написать менеджеру', url=manager_url)
        kb.button(text='Назад', callback_data='faq')
        kb.adjust(1)
        return kb


class DynamicKeyboards:
    @staticmethod
    async def city_selection() -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        async with AsyncSessionLocal() as session:
            cities = await get_all_cities(session)

        for city_id, city_name in cities.items():
            kb.button(text=city_name, callback_data=f'change_city_{city_id}')

        kb.adjust(1)
        return kb

    @staticmethod
    def channel_link(channel_link: str, back_callback: str) -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Перейти в канал', url=channel_link)
        kb.button(text='Назад', callback_data=back_callback)
        kb.adjust(1)
        return kb

    @staticmethod
    def only_back(callback: str = 'start_menu') -> InlineKeyboardBuilder:
        kb = InlineKeyboardBuilder()
        kb.button(text='Назад', callback_data=callback)
        return kb
