import asyncio
import os
import sys
from pathlib import Path

import django
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from users.models import TgUser

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

TELEGRAM_API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TELEGRAM_API_TOKEN)

dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def handle_start_command(message: Message) -> None:
    if message.from_user is None:
        return

    _, is_new = await TgUser.objects.aget_or_create(
        tg_id=message.from_user.id,
        defaults=dict(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    )

    if is_new:
        await message.answer("Welcome to the bot!")
    else:
        await message.answer("You are already registered!")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
