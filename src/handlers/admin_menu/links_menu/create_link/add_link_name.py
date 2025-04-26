from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from src.states.create_link_states import CreateLinkMenuStates

from src.handlers.admin_menu.links_menu.create_link.create_link_menu import create_link_menu

from src.handlers.admin_menu.links_menu.links_menu_router import links_menu_router


@links_menu_router.callback_query(F.data == 'add_link_name')
async def add_link_name_entering(callback: CallbackQuery, state: FSMContext):

    """

    :param callback:
    :param state:
    :return:
    """

    # текст сообщения прислать имя ссылки
    message_text = ''.join(
        'Напишите короткое имя для ссылки, например вк таргет 52'
    )

    # создаем клавиатуру, кнопка назад в меню ссылок
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data='create_link_menu')

    # Отправляем сообщение с кнопкой назад
    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup())

    await state.update_data({'callback': callback})

    # включаем состояние на получение сообщения, которое будет именем ссылки
    await state.set_state(CreateLinkMenuStates.insert_name)


@links_menu_router.message(CreateLinkMenuStates.insert_name)
async def add_link_name_set(message: Message, state: FSMContext):

    """

    :param message:
    :param state:
    :return:
    """

    await message.delete()

    # достаем из состояния данные
    state_data = await state.get_data()

    # отключаем состояние insert_name
    await state.clear()

    # обновляем данные для создания пригласительной ссылки
    await state.update_data(state_data)
    await state.update_data({'link_name': message.text})

    await create_link_menu(callback=state_data['callback'], state=state)

