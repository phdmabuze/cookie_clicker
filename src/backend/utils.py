import logging

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from django.conf import settings
from django.utils import timezone


def get_time():
    return timezone.now()


async def check_tg_subscription(user_tg_id: int, channel_id: int | str):
    try:
        return (
        await Bot(settings.BOT_TOKEN).get_chat_member(chat_id=channel_id, user_id=user_tg_id)
    ).status not in [
        ChatMemberStatus.LEFT,
        ChatMemberStatus.KICKED,
    ]
    except Exception as e:
        logging.error(f"Error checking subscription for user {user_tg_id}: {e}")
        return False
