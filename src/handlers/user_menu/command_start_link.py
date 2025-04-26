from aiogram.filters import CommandObject, Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import *

from src.keyboards.user_menu_keyboards import *
from src.handlers.user_menu.user_menu_router import user_menu_router
from src.handlers.user_menu.command_start import start_command

from logs.logger_config import logger


@user_menu_router.message(CommandStart(deep_link=True))
async def start_command_link(message: Message, command: CommandObject, state: FSMContext):

    """

    :param state:
    :param message:
    :param command:
    :return:
    """

    if await state.get_value('user'):

        message_text = ''.join(
            ('<b>Привет 👋</b> \n\n',
             'Наш заботливый бот <b>ФудДвор</b> рад видеть тебя в нашей <b>совместной закупке</b> \n\n',
             'Здесь есть ответы на все вопросы и возможность заказать вкусные и свежие продукты по выгодной цене \n\n',
             'Сделайте свой первый заказ 👇'))

        # отправляем сообщение с кнопками
        await message.answer(message_text, reply_markup=start_main_menu_keyboard().as_markup())
        return

    # проверяем что в ссылке только 1 аргумент и это цифры
    if command.args and command.args.isdigit():

        # создаем сессию и достаем данные по id ссылки
        async with AsyncSessionLocal() as session:
            link_data = await get_link_by_id(session, int(command.args))

        # если ссылка создана и есть в базе, то берем значения и добавляем юзеру
        if link_data:
            # добавляем юзера в бд
            await add_user(session,
                           user_id=message.from_user.id,
                           join_link=link_data.link,
                           city=link_data.city,
                           platform=link_data.platform)
            # добавляем юзера в счетчик юзеров этой ссылки
            await add_user_to_link(session,
                                   user_id=message.from_user.id,
                                   link_str=link_data.link)

            # готовим сообщение как в user_menu
            message_text = ''.join(
                ('<b>Привет 👋</b> \n\n',
                 'Наш заботливый бот <b>ФудДвор</b> рад видеть тебя в нашей <b>совместной закупке</b> \n\n',
                 'Здесь ответы на все вопросы и возможность заказать вкусные и свежие продукты по выгодной цене \n\n',
                 'Сделайте свой первый заказ 👇'))

            # удаляем сообщение пользователя с командой старт
            await message.delete()
            # отправляем сообщение с кнопками
            await message.answer(message_text, reply_markup=start_main_menu_keyboard().as_markup())
            return

        # если такой ссылки нет в базе, просто добавляем юзера
        else:
            await start_command(message)
            return
