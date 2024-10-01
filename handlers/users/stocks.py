from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import back_to_menu
from keyboards.inline.stocks_keyboard import stocks_inline_keyboard, stocks_callback_data
from loader import dp, db, bot


@dp.message_handler(text="💰 Aksiyalar", state="*")
async def get_stocks(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    stocks = await db.select_all_stocks()
    if not stocks:
        await message.answer("Hali aksiyalar mavjud emas", reply_markup=back_to_menu)
        return
    stocks_list = []
    for stock in stocks:
        stocks_list.append(stock['id'])

    stock_id = stocks_list[0]
    stocks = await db.select_stock(id=stock_id)
    tr = 0
    while not stocks:
        tr += 1
        stock_id = stocks_list[tr]
        stocks = await db.select_stock(id=stock_id)
    stock = stocks[0]
    image = stock['image_id']

    product_name = stock['product_name']
    description = stock['description']
    time_limit = stock['time_limit']
    created_at = stock['created_at']
    limit = created_at + time_limit
    limit = limit + timedelta(hours=5)

    text = (f"🛒 Mahsulot: {product_name}\n"
            f"📃 Izoh: {description}\n"
            f"⏱️ Aksiya tugash vaqti: {(limit).strftime('%d - %B %H:%M').lstrip('0')}")

    markup = await stocks_inline_keyboard(stock_tr=tr, stocks_list=stocks_list)

    await message.answer_photo(
        photo=image,
        caption=text,
        reply_markup=markup
    )


@dp.callback_query_handler(stocks_callback_data.filter())
async def next_or_previous_stocks(call: types.CallbackQuery, callback_data: dict):
    tr = int(callback_data.get('tr'))
    stocks_list = callback_data.get('stocks')
    stocks_list = stocks_list[1: len(stocks_list) - 1]
    stocks_list = stocks_list.split(', ')
    stocks_list = list(map(int, stocks_list))

    len_stock_list = len(stocks_list)
    if tr >= len_stock_list:
        tr = 0
    elif tr < 0:
        tr = len_stock_list - 1

    stock_id = stocks_list[tr]

    stocks = await db.select_stock(id=stock_id)
    while not stocks:
        tr += 1
        stock_id = stocks_list[tr]
        stocks = await db.select_stock(id=stock_id)
    stock = stocks[0]
    image = stock['image_id']
    product_name = stock['product_name']
    description = stock['description']
    time_limit = stock['time_limit']
    created_at = stock['created_at']
    limit = created_at + time_limit
    limit = limit + timedelta(hours=5)

    text = (f"🛒 Mahsulot: {product_name}\n"
            f"📃 Izoh: {description}\n"
            f"⏱️ Aksiya tugash vaqti: {limit.strftime('%d - %B %H:%M').lstrip('0')}")

    markup = await stocks_inline_keyboard(stock_tr=tr, stocks_list=stocks_list)

    await call.message.answer_photo(
        photo=image,
        caption=text,
        reply_markup=markup
    )
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
