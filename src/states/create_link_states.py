from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class CreateLinkMenuStates(StatesGroup):
    insert_name = State()
    insert_city = State()
    insert_platform = State()
