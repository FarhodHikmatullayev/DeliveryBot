import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.confirm_stocks import edit_stock_keyboard, next_keyboard_button, create_stock_keyboard
from keyboards.default.main_menu import back_to_menu
from keyboards.default.stocks_for_admin import actions_keyboard_for_stocks
from keyboards.default.stocks_list import stocks_list_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from states.stocks_states import UpdateStockState, DeleteStockState
from loader import dp, db, bot
from data.config import ADMINS


@dp.message_handler(text="🖋️ O'zgartirish", state=UpdateStockState.stock_id)
async def update_stock(message: types.Message, state: FSMContext):
    await message.answer(text="📝 Aksiyadagi mahsulot uchun yangi nom kiriting.\n"
                              "Agar mahsulot nomini o'zgartirmoqchi bo'lmasangiz 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_keyboard_button)
    await UpdateStockState.product_name.set()


@dp.message_handler(text="🖋️ O'zgartirish", state='*')
async def edit_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    markup = await stocks_list_keyboard()
    await message.answer(text="O'zgartirmoqchi bo'lgan aksiyangizni tanlang 👇", reply_markup=markup)
    await UpdateStockState.stock_id.set()


@dp.message_handler(text="🔙 Orqaga", state=UpdateStockState.stock_id)
async def back_to_actions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=actions_keyboard_for_stocks)


@dp.message_handler(text="🔙 Aksiyalarga qaytish", state=UpdateStockState.stock_id, user_id=ADMINS)
async def back_to_stocks_list(message: types.Message, state: FSMContext):
    markup = await stocks_list_keyboard()
    await message.answer(text="O'zgartirmoqchi bo'lgan aksiyangizni tanlang 👇", reply_markup=markup)
    await UpdateStockState.stock_id.set()


@dp.message_handler(state=UpdateStockState.stock_id)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    data = await state.get_data()

    stocks = await db.select_stock(product_name=product_name)
    if stocks:
        stock = stocks[0]
        stock_id = stock['id']
        stock_time_limit = stock['time_limit']
        stock_description = stock['description']
        stock_image_id = stock['image_id']
        stock_created_time = stock['created_at']

        await state.update_data(stock_id=stock_id)
        await state.update_data(product_name=product_name)
        await state.update_data(image_id=stock_image_id)
        await state.update_data(description=stock_description)
        await state.update_data(time_limit=stock_time_limit)

        text = (f"🛒 Mahsulot: {product_name}\n"
                f"📃 Izoh: {stock_description}\n"
                f"⏱️ Aksiya aktivlik muddati: {stock_time_limit}\n"
                f"📆 Aksiya yaratilgan vaqt: {stock_created_time.strftime('%d - %B %H:%M').lstrip('0')}")

        await message.answer_photo(
            photo=stock_image_id,
            caption=text,
        )
        await message.answer(text="💬 Aksiyani o'zgartirasizmi?\n"
                                  "O'zgartirish tumasini bosing 👇", reply_markup=edit_stock_keyboard)

    else:
        await message.answer(text="Bu aksiya o'chirib yuborilgan", reply_markup=back_to_menu)


@dp.message_handler(state=UpdateStockState.product_name, text="🔜 Keyingi")
@dp.message_handler(state=UpdateStockState.product_name)
async def get_new_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    if product_name != "🔜 Keyingi":
        await state.update_data(product_name=product_name)
    await message.answer(text="📷 Aksiya uchun yangi rasm yuboring.\n"
                              "Agar aksiya rasmini o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_keyboard_button)
    await UpdateStockState.image_id.set()


@dp.message_handler(state=UpdateStockState.image_id, text="🔜 Keyingi")
@dp.message_handler(state=UpdateStockState.image_id, content_types=types.ContentType.PHOTO)
async def get_new_image_id(message: types.Message, state: FSMContext):
    try:
        if message.text != "🔜 Keyingi":
            image_id = message.photo[-1].file_id
            await state.update_data(image_id=image_id)
    except:
        pass
    await message.answer(text="✍️ Aksiya uchun yangi izoh yozing.\n"
                              "Agar aksiya izohini o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_keyboard_button)
    await UpdateStockState.description.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=UpdateStockState.image_id)
async def get_new_image_id(message: types.Message, state: FSMContext):
    await message.answer(text="⚠️ Siz rasm kiritmadingiz\n"
                              "Iltimos, rasm kiriting", reply_markup=back_to_menu)


@dp.message_handler(state=UpdateStockState.description, text="🔜 Keyingi")
@dp.message_handler(state=UpdateStockState.description)
async def get_new_description(message: types.Message, state: FSMContext):
    description = message.text
    if description != "🔜 Keyingi":
        await state.update_data(description=description)
    await message.answer(text="✍️ Aksiya uchun yangi amal qilish muddati kiriting.\n"
                              "Masalan: (12 soat, 1 kun, 2 kun, 3 oy, 4 yil)\n"
                              "Agar aksiya amal qilish muddatini o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_keyboard_button
                         )
    await UpdateStockState.time_limit.set()


@dp.callback_query_handler(text='yes', state=UpdateStockState.time_limit)
async def edit_stock(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    stock_id = data.get("stock_id")
    product_name = data.get("product_name")
    image_id = data.get("image_id")
    description = data.get("description")
    time_limit = data.get("time_limit")

    stock = await db.update_stock(
        stock_id=stock_id,
        product_name=product_name,
        image_id=image_id,
        description=description,
        time_limit=time_limit
    )
    await call.message.answer(text="✅ Aksiya muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=UpdateStockState.time_limit)
async def cancel_editing_stock(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'zgartirishni rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateStockState.time_limit, text="🔜 Keyingi")
@dp.message_handler(state=UpdateStockState.time_limit)
async def get_new_time_limit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_name = data.get("product_name")
    image_id = data.get("image_id")
    description = data.get("description")
    time_limit = data.get("time_limit")
    limit = message.text
    if limit != "🔜 Keyingi":
        limit = limit.split()
        try:
            limit[0] = int(limit[0])
            if limit[1] not in ['soat', 'kun', 'oy', 'yil']:
                text = ("⚠️ Siz muddatni notog'ri kiritdingiz\n"
                        "Quyidagi kabi kiriting\n"
                        "'son' orada bitta bo'sh joy 'kun oy yil soat kabilardan birini tanlash kerak'")
                await message.answer(text=text, reply_markup=back_to_menu)
                return
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

                await message.answer(text="Aksiya o'zgarishlardan so'ng quyidagicha bo'ladi👇")
                text = (f"🛒 Mahsulot nomi: {product_name}\n"
                        f"📃 Izoh: {description}\n"
                        f"⏱️ Amal qilish muddati: {time_limit}\n")
                await message.answer_photo(photo=image_id, caption=text)
                await message.answer(text="Saqlashni xohlaysizmi? ", reply_markup=confirm_keyboard)
                return
        except:
            text = ("⚠️ Siz muddatni notog'ri kiritdingiz\n"
                    "Quyidagi kabi kiriting\n"
                    "'son' orada bitta bo'sh joy 'kun oy yil soat kabilardan birini tanlash kerak'")
            await message.answer(text=text, reply_markup=back_to_menu)

    await message.answer(text="Aksiya o'zgarishlardan so'ng quyidagicha bo'ladi👇")
    text = (f"🛒 Mahsulot nomi: {product_name}\n"
            f"📃 Izoh: {description}\n"
            f"⏱️ Amal qilish muddati: {time_limit}\n")
    await message.answer_photo(photo=image_id, caption=text)
    await message.answer(text="Saqlashni xohlaysizmi? ", reply_markup=confirm_keyboard)
