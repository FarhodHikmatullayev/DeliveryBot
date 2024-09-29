from aiogram.dispatcher.filters.state import State, StatesGroup


class UserCreateStates(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    location = State()
