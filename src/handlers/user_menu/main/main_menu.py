from aiogram import F
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import start_main_menu_keyboard


@user_menu_router.callback_query(F.data == 'main_menu')
async def user_main_menu(callback: CallbackQuery):

    """

    :param callback:
    :return:
    """

    message_text = ''.join(
        ('<b>Привет 👋</b> \n\n',
         'Наш заботливый бот <b>ФудДвор</b> рад видеть тебя в нашей <b>совместной закупке</b> \n\n',
         'Здесь есть ответы на все вопросы и возможность заказать вкусные и свежие продукты по выгодной цене \n\n',
         'Сделайте свой первый заказ 👇'))

    # отправляем сообщение с кнопками
    await callback.message.edit_text(message_text, reply_markup=start_main_menu_keyboard().as_markup())

