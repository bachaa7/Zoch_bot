from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from aiogram import types

# scheduler = AsyncIOScheduler()
# scheduler.start()

# Пример функций-обработчиков для отправки напоминаний
async def send_water_reminder(chat_id: int, bot):
    await bot.send_message(chat_id, "💧 Пора выпить воду!")

async def send_sleep_reminder(chat_id: int, bot):
    await bot.send_message(chat_id, "😴 Пора готовиться ко сну!")

async def send_exercise_reminder(chat_id: int, bot):
    await bot.send_message(chat_id, "🏃 Пора сделать разминку!")

# Обёртка для запуска асинхронной функции в apscheduler
def wrap_async_job(async_func, bot, chat_id):
    async def job():
        await async_func(chat_id, bot)
    return job

class ReminderManager:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler

    # В методах используйте self.scheduler вместо глобального scheduler
    def add_reminder(self, chat_id: int, reminder_type: str, times: list[str]):
        base_id = f"{reminder_type}_{chat_id}"

        for job in self.scheduler.get_jobs():
            if job.id.startswith(base_id):
                self.scheduler.remove_job(job.id)

        job_func_map = {
            "water": send_water_reminder,
            "sleep": send_sleep_reminder,
            "exercise": send_exercise_reminder,
        }

        job_func = job_func_map.get(reminder_type)
        if not job_func:
            raise ValueError("Неподдерживаемый тип напоминания")

        for time_str in times:
            hour, minute = map(int, time_str.split(":"))
            job_id = f"{base_id}_{hour}_{minute}"

            self.scheduler.add_job(
                wrap_async_job(job_func, self.bot, chat_id),
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id,
                replace_existing=True,
            )

    def remove_reminders(self, chat_id: int, reminder_type: str):
        base_id = f"{reminder_type}_{chat_id}"
        for job in self.scheduler.get_jobs():
            if job.id.startswith(base_id):
                self.scheduler.remove_job(job.id)