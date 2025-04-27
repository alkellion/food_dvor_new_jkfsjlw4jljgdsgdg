from aiogram import F
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import branches_keyboard


@user_menu_router.callback_query(F.data == 'where_receive')
async def where_receive_message(callback: CallbackQuery):

    """

    Обработка кнопки или вопроса Где забрать товар?
    Здесь на первое время просто список всех ПВЗ
    В дальнейшем планировалось по городу выдавать и более красиво и информативно

    :param callback: callback
    :return:
    """

    message_text = ''.join((
        '<b>Пункты выдачи, где можно забрать заказ</b> \n',
        'А еще если нажать на адрес он скопируется ;) \n\n',
        '<b>Казань</b>\n',
        'Адрес: <code>ул. Большая 2</code> \n\n',
        '<b>Саранск</b>\n',
        'Адрес: <code>Московская 17</code> \n\n',
        '<b>Самара</b>\n',
        'Адрес: <code>Мирная 162</code> \n\n',
        '<b>Тольяти</b>\n',
        'Адрес: <code>Фрунзе 2А</code> \n\n',
        '<b>Пенза</b>\n',
        'Адрес: <code>Окружная 16</code> \n\n',
        '<b>Нижнй Новгород</b>\n',
        'Адрес: <code>Гордеевская 8</code> \n\n',
        '<b>Чебоксары</b>\n',
        'Адрес: <code>Московский проспект 40В</code>',
    ))

    keyboard = branches_keyboard()

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup(), disable_web_page_preview=True)
