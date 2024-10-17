import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from pytz import timezone

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
        stock_link = stock['products_url']

        await state.update_data(stock_id=stock_id)
        await state.update_data(product_name=product_name)
        await state.update_data(link=stock_link)

        text = (f"🛒 Mahsulot: {product_name}\n"
                f"📃 {stock_link}\n")

        await message.answer(
            text=text,
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
    await message.answer(text="📷 Aksiya uchun yangi link kiriting.\n"
                              "Agar aksiya linkini o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_keyboard_button)
    await UpdateStockState.link.set()


@dp.callback_query_handler(text='yes', state=UpdateStockState.link)
async def edit_stock(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    stock_id = data.get("stock_id")
    product_name = data.get("product_name")
    link = data.get("link")

    stock = await db.update_stock(
        stock_id=stock_id,
        product_name=product_name,
        products_url=link,
    )
    await call.message.answer(text="✅ Aksiya muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=UpdateStockState.link)
async def cancel_editing_stock(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'zgartirishni rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateStockState.link, text="🔜 Keyingi")
@dp.message_handler(state=UpdateStockState.link)
async def get_new_link(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    data = await state.get_data()
    product_name = data.get('product_name')

    await message.answer(text="Aksiya o'zgarishlardan so'ng quyidagicha bo'ladi👇")
    text = (f"🛒 Mahsulot nomi: {product_name}\n"
            f"📃 Mahsulot: {link}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi? ", reply_markup=confirm_keyboard)
