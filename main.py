import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
