from aiogram.types import CallbackQuery
from aiogram import F
from src.handlers.user_menu.user_menu_router import user_menu_router

from src.keyboards.user_menu_keyboards import pay_order_keyboard


@user_menu_router.callback_query(F.data == 'pay_order')
async def pay_order_message(callback: CallbackQuery):

    """

    Обработка кнопки Оплатиьт заказ

    :param callback: callback
    :return:
    """

    message_text = ''.join((
        '<b>Никакой предоплаты 🙅</b> \n\n',
        'Мы не берем предоплату, оплатить заказ можно наличными в пункте выдачи или курьеру \n\n',
        'Так вы не попадете на мошенников и сможете проверить заказ перед оплатой'
    ))

    keyboard = pay_order_keyboard()

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup(), disable_web_page_preview=True)
