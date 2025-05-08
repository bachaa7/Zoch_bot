import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv
from aiogram.types import Message
from ostis_client import connect_to_ostis  # Импортируем функцию подключения


from app.handlers import router as main_router
from app.definition_handler import router as definition_router

# Загрузка переменных окружения
load_dotenv()






async def main():
    # Подключаемся к OSTIS серверу
    connect_to_ostis()  # Подключение к серверу осуществляется в отдельной функции

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(main_router)         # основной роутер (start, help и т.д.)
    dp.include_router(definition_router)   # отдельный роутер для команды /define

    await dp.start_polling(bot)  # Запуск бота

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")


#source .venv/bin/activate
#deactivate
