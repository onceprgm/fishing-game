from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot import i18n
from bot.keyboards import language_keyboard, main_menu_keyboard
from bot.storage import db

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    user = message.from_user
    player = await db.get_or_create_player(user.id, user.username)
    if player["language"]:
        await message.answer(
            i18n.t("welcome", player["language"]),
            reply_markup=main_menu_keyboard(player["language"]),
        )
    else:
        await message.answer(
            "Выберите язык / Choose your language:",
            reply_markup=language_keyboard(),
        )


@router.callback_query(F.data.startswith("lang:"))
async def handle_language_choice(callback: CallbackQuery) -> None:
    language = callback.data.split(":", 1)[1]
    if language not in i18n.SUPPORTED_LANGUAGES:
        await callback.answer()
        return
    await db.set_language(callback.from_user.id, language)
    await callback.message.edit_text(
        i18n.t("welcome", language),
        reply_markup=main_menu_keyboard(language),
    )
    await callback.answer()
