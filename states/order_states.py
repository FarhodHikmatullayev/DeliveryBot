from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateOrderState(StatesGroup):
    products = State()
    location = State()
    phone_number = State()
    payment = State()
