from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu import menu
from loader import dp


@dp.message_handler(text='🔙 Bosh Menyu', state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    if str(message.from_user.id) in ADMINS:
        menu_keyboard = await menu(is_admin=True)
    else:
        menu_keyboard = await menu()
    await message.answer(text="Bo'limlardan birini tanlang 👇", reply_markup=menu_keyboard)
