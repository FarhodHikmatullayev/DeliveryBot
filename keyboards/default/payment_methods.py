from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

payment_methods_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Naqt"),
        ],
        [
            KeyboardButton(text="Terminal (Uzcard)"),
        ],
        [
            KeyboardButton(text="Click"),
        ],
    ]
)
