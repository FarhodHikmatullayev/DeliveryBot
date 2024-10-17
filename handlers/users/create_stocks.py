from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.confirm_stocks import create_stock_keyboard
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


@dp.message_handler(text="➕ Yana aksiya qo'shish", state="*")
@dp.message_handler(text="✨ Yangi yaratish", state='*')
async def create_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await message.answer(text="✏️ Aksiya nomini kiriting", reply_markup=back_to_menu)
    await CreateStockState.product_name.set()


@dp.message_handler(state=CreateStockState.product_name)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer(text="🔗 Aksiya linkini yuboring", reply_markup=back_to_menu)
    await CreateStockState.link.set()


@dp.callback_query_handler(text='yes', state=CreateStockState.link)
async def create_stock(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_name = data.get("product_name")
    link = data.get("link")
    stock = await db.create_stock(
        product_name=product_name,
        products_url=link,
    )
    await call.message.answer(text="✅ Aksiya saqlandi", reply_markup=create_stock_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=CreateStockState.link)
async def cancel_creating_stock(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlashni rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateStockState.link)
async def get_link(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    data = await state.get_data()
    product_name = data.get('product_name')
    text = (f"🛒 Aksiya nomi: {product_name}\n"
            f"🔗 {link}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi? ", reply_markup=confirm_keyboard)
