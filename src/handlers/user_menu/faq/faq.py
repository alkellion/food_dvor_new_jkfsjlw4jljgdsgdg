from aiogram import F
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import faq_keyboard


@user_menu_router.callback_query(F.data == 'faq')
async def faq_message(callback: CallbackQuery):

    """

    :param callback:
    :return:
    """

    message_text = ''.join(
        ('<b>Привет 👋</b> \n\n',
         'Наш заботливый бот <b>ФудДвор</b> рад видеть тебя в нашей <b>совместной закупке</b> \n\n',
         'Здесь есть ответы на все вопросы и возможность заказать вкусные и свежие продукты по выгодной цене \n\n',
         'Сделайте свой первый заказ 👇'))

    keyboard = faq_keyboard()

    # редактируем сообщение
    await callback.message.edit_text(text=message_text, reply_markup=keyboard.as_markup())

