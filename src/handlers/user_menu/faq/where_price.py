from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import channel_link_keyboard

from database.engine import AsyncSessionLocal


@user_menu_router.callback_query(F.data == 'where_price')
async def where_price_message(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки или вопроса Где смотреть цены

    :param state: для хранения быстрых данных
    :param callback: callback
    :return:
    """

    # достаем данные из состояния
    city = await state.get_value('city')

    message_text = ''.join((
        '<b>Как и где посмотреть цены? 👀</b> \n\n',
        f'Все актуальные цены, товары и новые поступления можно найти в <a href="{city.invite_link}">нашем канале</a> \n\n',
        'Цена есть в <u>каждом</u> посте с товаром'
    ))

    await callback.message.edit_text(message_text, reply_markup=channel_link_keyboard(city.invite_link, 'faq').as_markup(), disable_web_page_preview=True)

