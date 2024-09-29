import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu import back_to_menu
from keyboards.default.stocks_for_admin import actions_keyboard_for_stocks
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.stocks_states import CreateStockState


@dp.message_handler(text="⚙️ Aksiyalarni boshqarish", user_id=ADMINS, state="*")
async def create_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=actions_keyboard_for_stocks)


@dp.message_handler(text="✨ Yangi yaratish", state='*')
async def create_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await message.answer(text="Mahsulot nomini kiriting", reply_markup=back_to_menu)
    await CreateStockState.product_name.set()


@dp.message_handler(state=CreateStockState.product_name)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer(text="Aksiya uchun rasm kiriting", reply_markup=back_to_menu)
    await CreateStockState.image_id.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=CreateStockState.image_id)
async def get_image_id(message: types.Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image_id=image_id)
    await state.update_data(image_id=image_id)
    await message.answer(text="Aksiya uchun izoh yozing", reply_markup=back_to_menu)
    await CreateStockState.description.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=CreateStockState.image_id)
async def get_image_id(message: types.Message, state: FSMContext):
    await message.answer(text="Siz rasm kiritmadingiz\n"
                              "Iltimos, rasm kiriting", reply_markup=back_to_menu)


@dp.message_handler(state=CreateStockState.description)
async def get_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer(text="Ushbu aksiya qancha muddat amal qiladi?\n"
                              "Masalan: (12 soat, 1 kun, 2 kun, 3 oy, 4 yil)")
    await CreateStockState.time_limit.set()


@dp.callback_query_handler(text='yes', state=CreateStockState.time_limit)
async def create_stock(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_name = data.get("product_name")
    image_id = data.get("image_id")
    description = data.get("description")
    time_limit = data.get("time_limit")

    stock = await db.create_stock(
        product_name=product_name,
        image_id=image_id,
        description=description,
        time_limit=time_limit
    )
    await call.message.answer(text="Aksiya saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=CreateStockState.time_limit)
async def cancel_creating_stock(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="Saqlashni rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateStockState.time_limit)
async def get_time_limit(message: types.Message, state: FSMContext):
    limit = message.text
    limit = limit.split()
    try:
        limit[0] = int(limit[0])
        if limit[1] not in ['soat', 'kun', 'oy', 'yil']:
            text = ("⚠️ Siz muddatni notog'ri kiritdingiz\n"
                    "Quyidagi kabi kiriting\n"
                    "'son' orada bitta bo'sh joy 'kun oy yil soat kabilardan birini tanlash kerak'")
            await message.answer(text=text, reply_markup=back_to_menu)
        else:
            if limit[1] == 'soat':
                time_limit = datetime.timedelta(hours=limit[0])
            elif limit[1] == 'kun':
                time_limit = datetime.timedelta(days=limit[0])
            elif limit[1] == 'oy':
                time_limit = datetime.timedelta(days=limit[0] * 30)
            else:
                time_limit = datetime.timedelta(days=limit[0] * 365)
            await state.update_data(time_limit=time_limit)
            data = await state.get_data()
            product_name = data.get("product_name")
            image_id = data.get("image_id")
            description = data.get("description")
            await message.answer(text="Aksiya quyidagicha bo'ladi👇")
            text = (f"🛒 Mahsulot nomi: {product_name}\n"
                    f"📃 Izoh: {description}\n"
                    f"⏱️ Amal qilish muddati: {time_limit}\n")
            await message.answer_photo(photo=image_id, caption=text)
            await message.answer(text="Saqlashni xohlaysizmi? ", reply_markup=confirm_keyboard)

    except:
        ext = ("⚠️ Siz muddatni notog'ri kiritdingiz\n"
               "Quyidagi kabi kiriting\n"
               "'son' orada bitta bo'sh joy 'kun oy yil soat kabilardan birini tanlash kerak'")
        await message.answer(text=text, reply_markup=back_to_menu)
