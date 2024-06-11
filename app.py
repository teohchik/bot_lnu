# app.py
import asyncio
import logging

from aiogram import Bot, Dispatcher

from utils.config import CHAT_ID
from utils.config import TOKEN
from handlers import start, schedule, questionnaire

# Налаштування логгера
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_routers(
    start.router,
    schedule.router,
    questionnaire.router
)


async def main():
    await bot.send_message(CHAT_ID, "Бот запущено!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
