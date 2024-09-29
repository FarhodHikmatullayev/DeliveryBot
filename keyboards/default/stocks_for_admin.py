from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

actions_keyboard_for_stocks = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="✨ Yangi yaratish"),
        ],
        [
            KeyboardButton(text="🖋️ O'zgartirish"),
        ],
        [
            KeyboardButton(text="🗑️ O'chirish"),
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)
