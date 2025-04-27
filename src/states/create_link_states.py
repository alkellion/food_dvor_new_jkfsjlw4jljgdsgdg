from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class CreateLinkMenuStates(StatesGroup):

    """
    Класс состояний для меню создания ссылки.

    Этот класс используется для хранения значений при создании ссылки в процессе

    Состояния:
    - Ввод имени ссылки
    - Ввод города ссылки
    - Ввод платформы ссылки
    """

    insert_name = State()
    insert_city = State()
    insert_platform = State()
