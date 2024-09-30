from email.policy import default

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.confirm_creating_order import confirm_order, confirm_phone_number, send_order
from keyboards.default.main_menu import back_to_menu
from loader import dp, db, bot
from states.order_states import CreateOrderState


@dp.message_handler(text="🛒 Buyurtma berish", state="*")
async def start_creating_order(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await message.answer(text="Biz bilan buyurtma berish ancha oson")
    text = (f"Mahsulotlar ro'yxatini kiriting. Masalan:\n"
            f"1. Kartoshka 2kg\n"
            f"2. Guruch 1kg\n"
            f"3. Yog' 1litr\n"
            f"4. Go'sht 0.5kg(yoki yarim kilo)")

    await message.answer(
        text=text,
        reply_markup=back_to_menu
    )
    await CreateOrderState.products.set()


@dp.message_handler(text="🔙 Orqaga", state=CreateOrderState.products)
async def get_products_again(message: types.Message, state: FSMContext):
    text = (f"Mahsulotlar ro'yxatini kiriting. Masalan:\n"
            f"1. Kartoshka 2kg\n"
            f"2. Guruch 1kg\n"
            f"3. Yog' 1litr\n"
            f"4. Go'sht 0.5kg(yoki yarim kilo)")

    await message.answer(
        text=text,
        reply_markup=back_to_menu
    )
    await CreateOrderState.products.set()


@dp.message_handler(text="Davom etish 🔜", state=CreateOrderState.products)
async def get_phone_number(message: types.Message, state: FSMContext):
    await message.answer(
        text="📍 Manzilingizni kiriting",
        reply_markup=back_to_menu
    )
    await CreateOrderState.location.set()


@dp.message_handler(state=CreateOrderState.products)
async def create_order(message: types.Message, state: FSMContext):
    products = message.text
    await state.update_data(products=products)
    text = (f"📦 Sizning buyurtmangiz:\n"
            f"{products}\n")
    await message.answer(text=text)
    await message.answer(
        text="Barchasi to'g'rimi?\n"
             "👇 Agar tog'ri bo'lsa Davom etish tugmasini bosing\n"
             "👇 Xatolik mavjud bo'lsa, Orqaga tugmasini bosing",
        reply_markup=confirm_order
    )


@dp.message_handler(text="Raqamni o'zgartirish", state=CreateOrderState.location)
async def get_phone(message: types.Message, state: FSMContext):
    await message.answer(text="📞 Telefon raqamingizni kiriting:\n"
                              "Misol: +998901234567",
                         reply_markup=back_to_menu)
    await CreateOrderState.phone_number.set()


@dp.message_handler(text="Davom etish 🔜", state=CreateOrderState.location)
async def confirm_order_for_send(message: types.Message, state: FSMContext):
    data = await state.get_data()
    products = data.get("products")
    location = data.get("location")
    phone_number = data.get("phone_number")
    text = (f"🏠 Manzilingiz: {location}\n"
            f"☎️ Telefon raqamingiz: {phone_number}\n"
            f"📦 Mahsulotlar ro'yxati 👇\n"
            f"{products}\n")
    await message.answer(text=text, reply_markup=back_to_menu)
    await message.answer(text="Buyurtmani yuborishni xohlaysizmi?\n"
                              "👇 Yuborish tugmasini bosing", reply_markup=send_order)


@dp.message_handler(text="Yuborish 🚀", state=[CreateOrderState.phone_number, CreateOrderState.location])
async def create_and_send_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get("phone_number")
    location = data.get("location")
    products = data.get("products")
    user = await db.select_users(telegram_id=message.from_user.id)
    user = user[0]

    order = await db.create_order(
        user_id=user['id'],
        products=products,
    )

    text = (f"🆕 Yangi buyurtma\n"
            f"📦 Mahsulotlar:\n"
            f"{products}\n"
            f"🏠 Manzil: {location}\n"
            f"👤 Buyurtma egasi: {user['full_name']}\n"
            f"☎️ Tel: {phone_number}\n"
            f"⏱️ Vaqt: {order['created_at'].strftime('%d/%m/%Y %H:%M')}\n")
    await bot.send_message(chat_id=5757849246, text=text)

    await message.answer(text="✅ Buyurtmangiz yuborildi,\n"
                              "Tez orada adminlarimiz sizga bog'lanishadi 🙂", reply_markup=back_to_menu)

    await state.finish()


@dp.message_handler(state=CreateOrderState.location)
async def get_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    phone_number = user["phone"]
    await state.update_data(phone_number=phone_number)
    text = (f"Sizning raqamingiz hali ham {phone_number}mi?\n"
            f"👇 Iltimos agar raqamingiz o'zgarmagan bo'lsa Davom etish tugmasini bosing\n"
            f"👇 Agar raqamingiz o'zgargan bo'lsa, Raqamni o'zgartirish tugmasini bosing")

    await message.answer(
        text=text, reply_markup=confirm_phone_number
    )


@dp.message_handler(state=CreateOrderState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    products = data.get("products")
    location = data.get("location")
    text = (f"🏠 Manzilingiz: {location}\n"
            f"☎️ Telefon raqamingiz: {phone_number}\n"
            f"📦 Mahsulotlar ro'yxati 👇\n"
            f"{products}\n")
    await message.answer(text=text, reply_markup=back_to_menu)
    await message.answer(text="Buyurtmani yuborishni xohlaysizmi?\n"
                              "👇 Yuborish tugmasini bosing", reply_markup=send_order)
