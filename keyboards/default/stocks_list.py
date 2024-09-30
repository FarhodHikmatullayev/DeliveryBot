from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.html import avoid_wrapping

from loader import db


async def stocks_list_keyboard():
    stocks = await db.select_all_stocks()
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for stock in stocks:
        text_button = stock['product_name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup
