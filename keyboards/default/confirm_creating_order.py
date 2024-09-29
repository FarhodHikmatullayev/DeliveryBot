from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_order = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="🔙 Orqaga",
            ),
            KeyboardButton(
                text="Davom etish 🔜"
            )
        ]
    ]
)

confirm_phone_number = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Raqamni o'zgartirish"),
            KeyboardButton(text="Davom etish 🔜")
        ]
    ]
)

send_order = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
            KeyboardButton(text="Yuborish 🚀")
        ]
    ]
)
