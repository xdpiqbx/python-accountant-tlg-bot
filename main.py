import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers import router, db_obj
from dotenv import load_dotenv

load_dotenv()

dp = Dispatcher()

# Bot startup: Connect to database
async def on_startup():
    await db_obj.start_db()
    print("Bot started and DB connected.")

# Bot shutdown: Close database connection
async def on_shutdown():
    await db_obj.disconnect()
    print("Bot stopped and DB connection closed.")


async def main() -> None:
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)  # And the run events dispatching


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
