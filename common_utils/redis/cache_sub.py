from datetime import date, datetime, timedelta
import json
from common_utils.redis.client import redis_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from notification_service.main import send_email

from common_utils.redis import EmailReminder

from common_utils.utils.calculate_payday import date_to_timestamp, сounting_payment_day


from logs import logger

scheduler = AsyncIOScheduler()


async def add_reminder(
    email: str, sub_title: str, reminder_date: str, frequency_id: int
):
    reminder_data = EmailReminder(
        email=email, sub_title=sub_title, frequency_id=frequency_id
    )

    reminder_data_json = json.dumps(reminder_data.to_dict(), ensure_ascii=False)

    await redis_client.zadd("reminders", {reminder_data_json: reminder_date})


async def remove_reminder(email: str, sub_title: str, frequency_id: int):
    reminder_data = EmailReminder(
        email=email, sub_title=sub_title, frequency_id=frequency_id
    )
    reminder_data_json = json.dumps(reminder_data.to_dict(), ensure_ascii=False)

    await redis_client.zrem("reminders", reminder_data_json)


async def check_reminders():
    current_date = int(datetime.now().timestamp())

    logger.info("Checking reminders...")

    reminders = await redis_client.zrangebyscore("reminders", 0, current_date)

    if not reminders:
        logger.info("No reminders to send.")
        return

    for reminder in reminders:
        logger.info(f"Sending reminder: {reminder}")
        data = json.loads(reminder)

        email = data["email"]
        sub_title = data["sub_title"]
        frequency_id = data["frequency_id"]

        reminder = EmailReminder(
            email=email, sub_title=sub_title, frequency_id=frequency_id
        )

        await send_email(reminder)

        reminder_data_json = json.dumps(reminder.to_dict())

        await redis_client.zrem("reminders", reminder_data_json)

        await refresh_reminders(email, sub_title, frequency_id)


async def refresh_reminders(email: str, sub_title: str, frequency_id: int):
    next_payment_date = сounting_payment_day(frequency_id, date.today())

    # Calculate the reminder date (3 days before the next payment date)
    reminder_date = next_payment_date - timedelta(days=3)

    timestamp = date_to_timestamp(reminder_date)

    await add_reminder(email, sub_title, timestamp, frequency_id)


scheduler.add_job(check_reminders, "interval", seconds=10)
scheduler.start()
