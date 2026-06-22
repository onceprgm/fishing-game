import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.handlers import cast, start
from bot.scheduler import run_bite_notifier
from bot.storage import db


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await db.init_db()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(cast.router)
    notifier = asyncio.create_task(run_bite_notifier(bot))
    try:
        await dp.start_polling(bot)
    finally:
        notifier.cancel()


if __name__ == "__main__":
    asyncio.run(main())
