from aiogram import executor
import asyncio
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.delete_stock_task import delete_stocks
from utils.set_bot_commands import set_default_commands
from keep_alive import keep_alive
from data.config import DEVELOPMENT_MODE

if not DEVELOPMENT_MODE:
    keep_alive()


async def on_startup(dispatcher):
    await db.create()
    await set_default_commands(dispatcher)

    asyncio.create_task(delete_stocks())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
