import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.confirm_stocks import delete_stock_keyboard
from keyboards.default.main_menu import menu, back_to_menu
from keyboards.default.stocks_for_admin import actions_keyboard_for_stocks
from keyboards.default.stocks_list import stocks_list_keyboard
from loader import dp, db
from states.stocks_states import DeleteStockState


@dp.message_handler(text="🗑️ O'chirish", state=DeleteStockState.product_name)
async def delete_stock(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_name = data.get("product_name")
    stocks = await db.select_stock(product_name=product_name)
    if stocks:
        stock = stocks[0]
        stock_id = stock['id']
        await db.delete_stock(stock_id=stock_id)
        await message.answer(text="📣 Aksiya muvaffaqiyatli o'chirildi ✅", reply_markup=back_to_menu)
    else:
        await message.answer(text="📢 Bu aksiya allaqachon o'chirilgan", reply_markup=back_to_menu)
    await state.finish()


@dp.message_handler(text="🗑️ O'chirish", user_id=ADMINS, state='*')
async def delete_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    markup = await stocks_list_keyboard()
    await message.answer(text="O'chirmoqchi bo'lgan aksiyangizni tanlang 👇", reply_markup=markup)
    await DeleteStockState.product_name.set()


@dp.message_handler(text="🔙 Orqaga", state=DeleteStockState.product_name)
async def back_to_actions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=actions_keyboard_for_stocks)


@dp.message_handler(text="🔙 Aksiyalarga qaytish", state=DeleteStockState.product_name, user_id=ADMINS)
async def back_to_stocks_list(message: types.Message, state: FSMContext):
    markup = await stocks_list_keyboard()
    await message.answer(text="O'chirmoqchi bo'lgan aksiyangizni tanlang 👇", reply_markup=markup)
    await DeleteStockState.product_name.set()


@dp.message_handler(state=DeleteStockState.product_name)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    data = await state.get_data()


    stocks = await db.select_stock(product_name=product_name)
    if stocks:
        stock = stocks[0]
        stock_time_limit = stock['time_limit']
        stock_description = stock['description']
        stock_image_id = stock['image_id']
        stock_created_time = stock['created_at']
        stock_created_time += datetime.timedelta(hours=5)

        text = (f"🛒 Mahsulot: {product_name}\n"
                f"📃 Izoh: {stock_description}\n"
                f"⏱️ Aksiya aktivlik muddati: {stock_time_limit}\n"
                f"📆 Aksiya yaratilgan vaqt: {stock_created_time.strftime('%d - %B %H:%M').lstrip('0')}")

        await message.answer_photo(
            photo=stock_image_id,
            caption=text,
        )
        await message.answer(text="💬 Aksiyani o'shirilsinmi?\n"
                                  "O'chirish tumasini bosing 👇", reply_markup=delete_stock_keyboard)

    else:
        await message.answer(text="Bu aksiya o'chirib yuborilgan", reply_markup=back_to_menu)
