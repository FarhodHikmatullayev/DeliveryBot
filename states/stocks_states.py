from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateStockState(StatesGroup):
    product_name = State()
    image_id = State()
    description = State()
    time_limit = State()


class UpdateStockState(StatesGroup):
    stock_id = State()
    product_name = State()
    image_id = State()
    description = State()
    time_limit = State()


class DeleteStockState(StatesGroup):
    product_name = State()
