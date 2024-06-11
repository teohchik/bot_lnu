from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    faculty = State()
    course = State()
    group = State()