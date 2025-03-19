import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers import router
from app.accountant_db import start_db
from dotenv import load_dotenv

load_dotenv()


dp = Dispatcher()


async def main() -> None:
    await start_db()
    dp.include_router(router)
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)  # And the run events dispatching


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
