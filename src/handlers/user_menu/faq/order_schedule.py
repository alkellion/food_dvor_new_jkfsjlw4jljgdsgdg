from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import channel_link_keyboard


@user_menu_router.callback_query(F.data == 'order_schedule')
async def order_schedule_message(callback: CallbackQuery, state: FSMContext):

    """

    Обработка кнопки или вопроса Когда закупка

    :param state: для хранения быстрых данных
    :param callback: callback
    :return:
    """

    # получаем данные пользователя и ссылку на канал заранее
    city = await state.get_value('city')

    # готовим сообщение
    message_text = ''.join((
        '<b>Когда мы создаем закупки?</b> \n\n',
        'С <u>понедельника</u> по <u>вторник</u> публикуем и принимаем заявки на продукты этой недели \n'
        'Но иногда можем принимать заказы и в среду :) \n\n'
        '❗️Некоторые товары <u>сезонные</u> и не доступны для заказа\n'
        f'❗️Следите за новостями и обновлениями в нашем <a href="{city.invite_link}">канале</a>'
    ))

    await callback.message.edit_text(message_text, reply_markup=channel_link_keyboard(city.invite_link, 'faq').as_markup(), disable_web_page_preview=True)
