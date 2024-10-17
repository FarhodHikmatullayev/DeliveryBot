import asyncio
import logging
from pytz import timezone
from data.config import ADMINS
from loader import db, bot
import datetime


async def delete_stocks():
    tz = timezone('UTC')

    while True:
        all_stocks = await db.select_all_stocks()
        for stock in all_stocks:
            stock_time_limit = stock['time_limit']
            stock_created_at = stock['created_at'].replace(tzinfo=tz)
            deleting_time = stock_time_limit + stock_created_at

            # deleting_time = deleting_time.astimezone(tz) + datetime.timedelta(hours=5)

            if deleting_time < datetime.datetime.now(tz):

                stock_id = stock['id']
                stock_product_name = stock['product_name']
                await db.delete_stock(stock_id=stock_id)
                text = (f"🛍️ Mahsulot nomi: {stock_product_name} \n"
                        f"⏰ Aksiya muddati tugadi\n"
                        f"🗑️ Aksiya o'chirib yuborildi")
                for admin in ADMINS:
                    try:
                        await bot.send_message(chat_id=admin, text=text)

                    except Exception as err:
                        logging.exception(err)
        await asyncio.sleep(60)
