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

edit_stock_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Aksiyalarga qaytish"),
            KeyboardButton(text="🖋️ O'zgartirish")
        ]
    ]
)

create_stock_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Yana aksiya qo'shish"),
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)

next_keyboard_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton("🔜 Keyingi")
        ]
    ]
)
