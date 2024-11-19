import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
from handlers import *


load_dotenv()
BOT_TOKEN = os.getenv('API_TELEGRAM_TOKEN')

logging.basicConfig(level=logging.INFO)


dp = Dispatcher()


async def main():
    # Регистрация обработчиков
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук, если он был установлен
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())