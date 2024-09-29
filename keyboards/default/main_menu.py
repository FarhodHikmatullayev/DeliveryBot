from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def menu(is_admin=False):
    if is_admin:
        return menu_for_admins
    else:
        return basic_menu


menu_for_admins = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="💰 Aksiyalar"),
        ],
        [
            KeyboardButton(text="🛒 Buyurtma berish"),
        ],
        [
            KeyboardButton(text="⚙️ Aksiyalarni boshqarish"),
        ]
    ]
)

basic_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="💰 Aksiyalar"),
        ],
        [
            KeyboardButton(text="🛒 Buyurtma berish"),
        ],
    ]
)

back_to_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)
