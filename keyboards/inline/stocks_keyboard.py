from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

stocks_callback_data = CallbackData('stocks', 'tr', 'stocks')


async def stocks_inline_keyboard(stock_tr: int, stocks_list: List[int]):
    print("stock_tr", stock_tr)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data=stocks_callback_data.new(tr=stock_tr - 1, stocks=stocks_list)
                ),
                InlineKeyboardButton(
                    text="🔜 Oldinga",
                    callback_data=stocks_callback_data.new(tr=stock_tr + 1, stocks=stocks_list)
                )
            ]
        ]
    )
    return markup
