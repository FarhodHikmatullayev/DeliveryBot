from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateStockState(StatesGroup):
    product_name = State()
    link = State()



class UpdateStockState(StatesGroup):
    stock_id = State()
    product_name = State()
    link = State()



class DeleteStockState(StatesGroup):
    product_name = State()
