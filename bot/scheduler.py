import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Bot

from bot import i18n
from bot.keyboards import waiting_keyboard
from bot.storage import db

POLL_INTERVAL_SECONDS = 15

logger = logging.getLogger(__name__)


async def run_bite_notifier(bot: Bot) -> None:
    while True:
        try:
            await _notify_due(bot)
        except Exception:
            logger.exception("bite notifier tick failed")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def _notify_due(bot: Bot) -> None:
    now = datetime.now(timezone.utc).timestamp()
    for row in await db.due_casts(now):
        lang = row["language"] or i18n.DEFAULT_LANGUAGE
        try:
            await bot.send_message(
                row["user_id"],
                i18n.t("bite", lang),
                reply_markup=waiting_keyboard(lang),
            )
        except Exception:
            logger.exception("failed to notify user %s", row["user_id"])
        await db.mark_notified(row["user_id"])
