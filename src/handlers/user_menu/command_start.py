from aiogram.filters import CommandObject, Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import *

from src.keyboards.user_menu_keyboards import *
from src.handlers.user_menu.user_menu_router import user_menu_router

from src.handlers.user_menu.main.main_menu import user_main_menu

from logs.logger_config import logger


@user_menu_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):

    """

    Обработка просто команды старт, без ссылки.
    Записываем в базу пользователя, если его нет, вносим данные.
    Если уже есть, то просто отправляем стартовое сообщение


    :param message: Объект сообщения
    :param state: Для хранения быстрых данных
    :return:

    """

    if await state.get_value('user'):

        message_text = ''.join(
            ('<b>Привет 👋</b> \n\n',
             'Наш заботливый бот <b>ФудДвор</b> рад видеть тебя в нашей <b>совместной закупке</b> \n\n',
             'Здесь есть ответы на все вопросы и возможность заказать вкусные и свежие продукты по выгодной цене \n\n',
             'Сделайте свой первый заказ 👇'))

        # удаляем сообщение пользователя с командой старт
        await message.delete()
        # отправляем сообщение с кнопками
        await message.answer(message_text, reply_markup=start_main_menu_keyboard().as_markup())
        return

    async with AsyncSessionLocal() as session:

        await add_user(session,
                       user_id=message.from_user.id,
                       join_link=None,
                       city=None,
                       platform=None)

        # создаем сообщение с выбором города и редактируем текст
        message_text = ''.join((
            '<b>Ой, кажется мы не смогли определить ваш город</b> \n\n',
            'Укажите с какого вы города с помощью кнопок ниже \n',
            'Так бот будет работать корректнее :)'
        ))

        # удаляем сообщение пользователя с командой старт
        await message.delete()
        await message.answer(message_text, reply_markup=(await city_selection_keyboard()).as_markup())
        return
