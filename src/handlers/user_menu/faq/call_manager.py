from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import call_manager_keyboard


@user_menu_router.callback_query(F.data == 'call_manager')
async def call_manager_message(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки Связаться с менеджером

    :param callback: callback
    :param state: для хранения быстрых данных
    :return:
    """

    # получаем из базы нужные для работы данные, пользователя и города (канала)
    city = await state.get_value('city')

    # готовим сообщения и вставялем нужные данные
    message_text = ''.join((
        '<b>Связаться с менеджером</b> \n\n',
        f'За каждым городом следит свой <a href="{city.manager}">менеджер</a> \n',
        f'Написать менеджеру города {city.city}?'
    ))

    # пулим сообщение
    await callback.message.edit_text(message_text, reply_markup=call_manager_keyboard(city.manager).as_markup(), disable_web_page_preview=True)
