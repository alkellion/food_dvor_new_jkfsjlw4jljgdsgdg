from aiogram.types import CallbackQuery
from aiogram import F
from src.handlers.user_menu.user_menu_router import user_menu_router

from src.keyboards.user_menu_keyboards import delivery_keyboard


@user_menu_router.callback_query(F.data == 'delivery')
async def delivery_message(callback: CallbackQuery):

    """


    :param callback:
    :return:
    """

    message_text = ''.join((
        '<b>Доставим до двери! 🚚</b> \n\n',
        'Если у вас нет возможности приехать в ПВЗ – мы отправим заказ до двери \n',
        'Стоимость 300 рублей независимо от кол-ва товара \n\n',
        '❗️ Доставка в пятницу и субботу, до последнего заказа'
    ))

    keyboard = delivery_keyboard()

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup(), disable_web_page_preview=True)
