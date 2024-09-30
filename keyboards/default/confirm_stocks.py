from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

delete_stock_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Aksiyalarga qaytish"),
            KeyboardButton(text="🗑️ O'chirish")
        ]
    ]
)
