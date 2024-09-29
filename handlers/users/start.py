from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.main_menu import menu
from loader import dp, db, bot
from states.user_states import UserCreateStates


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if users:
        user = users[0]
        full_name = user['full_name']
        first_name = full_name.split()[0]
        await message.reply(text=f"👋 Salom {first_name}!\n"
                                 f"Botimizga xush kelibsiz")
        if str(message.from_user.id) in ADMINS:
            menu_keyboard = await menu(is_admin=True)
        else:
            menu_keyboard = await menu()
        await message.answer(
            text=f"Bo'limlardan birini tanlang 👇",
            reply_markup=menu_keyboard
        )
    else:
        text = (f"👋 Salom, botimizga xush kelibsiz!\n"
                f"Botimizdan foydalanish uchun ismingizni kiriting.")

        await message.answer(text)
        await UserCreateStates.first_name.set()


@dp.message_handler(state=UserCreateStates.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    text = "Familiyangizni kiriting"
    await message.answer(text)
    await UserCreateStates.last_name.set()


@dp.message_handler(state=UserCreateStates.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    text = ("Sizga bog'lana olishimiz uchun telefon raqam kiriting\n"
            "Misol: +998901234567")
    await message.answer(text)
    await UserCreateStates.phone_number.set()


@dp.message_handler(state=UserCreateStates.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    full_name = f"{first_name} {last_name}"
    user = await db.create_user(
        telegram_id=message.from_user.id,
        full_name=full_name,
        phone=phone_number,
        username=message.from_user.username,
    )
    await state.finish()
    await message.answer(text="Siz botdan muvaffaqiyatli ro'yxatdan o'tdingiz!")
    if str(message.from_user.id) in ADMINS:
        menu_keyboard = await menu(is_admin=True)
    else:
        menu_keyboard = await menu()
    await message.answer(
        text=f"Bo'limlardan birini tanlang 👇",
        reply_markup=menu_keyboard
    )
