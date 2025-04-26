from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.user_menu.user_menu_router import user_menu_router
from src.keyboards.user_menu_keyboards import about_keyboard


@user_menu_router.callback_query(F.data == 'about')
async def about_message(callback: CallbackQuery, state: FSMContext):

    """


    :param callback:
    :param state:
    :return:
    """

    user_data = await state.get_value('user')
    city = await state.get_value('city')

    message_text = ''.join((
        '<b>Что такое ФудДвор и что предлагаем?</b> \n\n',
        'Мы компания, которая на протяжении многих лет выбирает и доставляет самые свежие и вкусные продукты из разных стран, например Индии, Таиланда, Азии, Азербайджана, Египта и других \n\n'
        '<b>У нас вы можете заказать</b> \n'
        '– Фрукты и овощи: от мандаринов до маракуйи \n'
        '– Ягоды: от брусники до клюквы \n'
        '– Рыба и морепродукты: от форели до кальмара \n'
        '– Икра: горбуши, нерки, кеты \n'
        '– Орехи и сухофрукты: от фундука до пекана \n'
        '– Деликатесы \n\n'
        '<b>Принимаем заказы каждую неделю</b> \n'
        f'О начале закупок, новых товарах и других новостях рассказываем в <a href="{city.invite_link}">нашем канале</a> \n\n'
        '<b>Больше о нашей компании можно прочитать тут @ArtelHoum</b>'
    ))

    keyboard = about_keyboard(city.invite_link)

    await callback.message.edit_text(message_text, reply_markup=keyboard.as_markup(), disable_web_page_preview=True)
