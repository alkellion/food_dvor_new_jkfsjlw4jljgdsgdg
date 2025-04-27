from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import channel_link_keyboard


@user_menu_router.callback_query(F.data == 'min_weigh')
async def min_weigh_message(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки или вопроса Можно поштучно?

    :param state: Для хранения быстрых данных
    :param callback: callback
    :return:
    """

    # достаем данные из состояния
    city = await state.get_value('city')

    # вставляем ссылку канала
    message_text = ''.join((
        '<b>Можно ли купить товар поштучно?</b> \n\n',
        'Жаль, но так не получится :( \n',
        'Каждый товар имеет минимальный объем для заказа, где-то 500гр, где-то 5кг \n\n',
        f'Минимальный объем для заказа <u>всегда</u> указываем в посте с товаров в <a href="{city.invite_link}">нашем канале</a>'
    ))

    await callback.message.edit_text(message_text, reply_markup=channel_link_keyboard(city.invite_link, 'faq').as_markup(), disable_web_page_preview=True)
