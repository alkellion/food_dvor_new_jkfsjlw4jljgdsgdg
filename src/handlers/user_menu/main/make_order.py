from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import make_order_keyboard

from database.crud import get_user, get_city_link
from database.engine import AsyncSessionLocal

from logs.logger_config import logger


@user_menu_router.callback_query(F.data == 'make_order')
async def make_order_message(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки Сделать заказ или За покупками
    В сообщении помещаем ссылку на канал, где происходит заказ

    :param callback: callback
    :param state: используем для быстрых данных
    :return:
    """

    city = await state.get_value('city')

    message_text = ''.join((
        '<b>Как заказать продукты? 🛍</b> \n\n',
        f'Переходите и подписывайтесь на наш <a href="{city.invite_link}">канал ФудДвор</a> \n',
        'Выбирайте любой товар и пишите в комментарии: \n\n',
        '👉 Сколько товара хотите заказать \n',
        '👉 Номер телефона для связи \n',
        '👉 Для доставки заказа до двери напишите "Доставка" \n\n',
        '❗️ Если комментарии закрыты или не нашли нужный товар: <i>он пока недоступен</i> \n',
        '❗️ Следите за новостями в канале о начале закупок'
    ))

    keyboard = make_order_keyboard(city.invite_link)

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup(), disable_web_page_preview=True)
