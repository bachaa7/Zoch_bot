import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router as main_router
from app.definition_handler import router as definition_router
from app.reminder_handler import ReminderManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import app.reminder_instance as reminder_instance

from ostis_client import connect_to_ostis

from app.rag_handlers import router as rag_router
from app.rag_creation_handlers import router as rag_creation_router  # Новый импорт

load_dotenv()

async def main():
    connect_to_ostis()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    # Создаем scheduler внутри event loop
    scheduler = AsyncIOScheduler()
    scheduler.start()

    reminder_manager = ReminderManager(bot, scheduler)
    reminder_instance.reminder_manager = reminder_manager

    dp.include_router(main_router)
    dp.include_router(definition_router)
    dp.include_router(rag_router)
    dp.include_router(rag_creation_router)  # Регистрируем новый роутер

    # Если нужно, сохраните reminder_manager куда-то глобально или в app.reminder_instance
    # Например:
    # from app import reminder_instance
    # reminder_instance.reminder_manager = reminder_manager

    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
